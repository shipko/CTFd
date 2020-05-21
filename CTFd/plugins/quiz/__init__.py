import os
import enum
import json
import yaml
import datetime
from random import shuffle
from flask import abort, render_template, redirect, request, session
from CTFd.models import db, Challenges
from CTFd.utils import markdown
from CTFd.utils.user import get_current_user
from CTFd.plugins import bypass_csrf_protection
from CTFd.utils.decorators import authed_only
from CTFd.utils.security.csrf import generate_nonce


class QuizStatusEnum(enum.Enum):
    running = 'running'
    passed = 'passed'
    failed = 'failed'


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz = db.Column(db.String(100))
    user = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    data = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(
        db.Enum(QuizStatusEnum),
        default=QuizStatusEnum.running,
        nullable=False
    )

    def __init__(self, quiz: str, user: int):
        self.quiz = quiz
        self.user = user


class ChallengeQuiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenge = db.Column(db.Integer, db.ForeignKey("challenges.id", ondelete="CASCADE"))
    quiz = db.Column(db.String(100))

    def __init__(self, quiz: str, challenge: Challenges):
        self.quiz = quiz
        self.challenge = challenge


def load(app):
    app.db.create_all()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    @bypass_csrf_protection
    @app.route('/quiz/<string:quiz>/start', methods=['POST'])
    @authed_only
    def view_quiz_start(quiz):
        quiz_file = "{}.yml".format(quiz)
        quiz_file = os.path.join(dir_path, 'data', quiz_file)

        if not os.path.isfile(quiz_file):
            abort(404)

        session['quiz_' + quiz] = None

        challenge_quiz = ChallengeQuiz.query.filter_by(quiz=quiz).first()

        model = Quiz(quiz, get_current_user().id)
        model.data = json.dumps({'questions': {}})
        model.challenge = challenge_quiz.challenge

        db.session.add(model)
        db.session.commit()

        return redirect('/quiz/{}'.format(quiz))

    @app.route('/quiz/<string:quiz>', methods=['GET', 'POST'])
    @authed_only
    def view_quiz(quiz):
        session["nonce"] = generate_nonce()

        quiz_data = get_quiz_data_or_404(quiz)
        user_quest = Quiz.query.filter_by(quiz=quiz, user=get_current_user().id, status=QuizStatusEnum.running).first()

        quiz_started = user_quest is not None
        answered_question_count = 0

        if quiz_started:
            if request.method == 'POST':
                user_quest_json_data = json.loads(user_quest.data)

                user_answer = request.form.getlist('answer')
                user_answer = set(map(int, user_answer))

                current_question = quiz_data['questions'][get_current_question(quiz)]
                answers = current_question['answers']
                answers = set({i for i in range(len(answers))})

                answers = {current_question['content']: list(answers.intersection(user_answer))}
                user_quest_json_data['questions'].update(answers)

                user_quest.data = json.dumps(user_quest_json_data)
                db.session.add(user_quest)
                db.session.commit()

                set_current_question(quiz, None)

            user_progress = json.loads(user_quest.data)
            answered_question_count = len(user_progress['questions'])

            # print(answered_question_count, )
            if answered_question_count == quiz_data['questionsToAskCount']:
                return redirect('/quiz/{}/finish'.format(quiz))

            if get_current_question(quiz) is None:
                random_question = [[idx, q] for idx, q in enumerate(quiz_data['questions'])]
                shuffle(random_question)

                for el in random_question:
                    if el[1]['content'] not in user_progress['questions']:
                        set_current_question(quiz, el[0])
                        break
                else:
                    abort(500)

        return render_template('quiz-plugin/quiz.html',
                               quiz=quiz_data,
                               name=quiz,
                               num=answered_question_count,
                               started=quiz_started,
                               next=get_current_question(quiz),
                               markdown=markdown,
                               nonce=session['nonce'])

    @app.route('/quiz/<string:quiz>/finish', methods=['GET'])
    @authed_only
    def view_quiz_finish(quiz):
        user_quest = Quiz.query.filter_by(quiz=quiz, user=get_current_user().id).all()[-1]

        quiz_data = get_quiz_data_or_404(quiz)

        user_progress = json.loads(user_quest.data)
        answered_question_count = len(user_progress['questions'])

        if answered_question_count < quiz_data['questionsToAskCount']:
            return redirect('/quiz/{}'.format(quiz))

        quiz_data = get_quiz_data_or_404(quiz)
        challenge_quiz = ChallengeQuiz.query.filter_by(quiz=quiz).first()

        challenge = Challenges.query.filter_by(id=challenge_quiz.challenge).first()
        user_quest_json_data = json.loads(user_quest.data)

        correct_answer = 0
        for question in user_quest_json_data['questions']:
            original_question = list(filter(lambda i: i['content'] == question, quiz_data['questions']))[0]
            if type(original_question['correctAnswer']) == int:
                original = {original_question['correctAnswer']}
            else:
                original = set(original_question['correctAnswer'])

            user_answer = set(user_quest_json_data['questions'][question])

            if original == user_answer:
                correct_answer += 1

        if correct_answer >= quiz_data['goalCount']:
            user_quest.status = QuizStatusEnum.passed
        else:
            user_quest.status = QuizStatusEnum.failed

        db.session.add(user_quest)
        db.session.commit()

        return render_template('quiz-plugin/finish.html',
                               name=quiz,
                               quiz=quiz_data,
                               challenge=challenge,
                               correct=correct_answer)

    def get_quiz_data_or_404(quiz_name: str):
        quiz_file = "{}.yml".format(quiz_name)
        try:
            with open(os.path.join(dir_path, 'data', quiz_file), 'r', encoding="utf-8") as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
                    abort(500)
        except FileNotFoundError:
            abort(404)
        except Exception as e:
            print(e)
            abort(500)

    def get_current_question(quiz_name):
        key = 'quiz_' + quiz_name
        return session[key] if key in session else None

    def set_current_question(quiz_name, value):
        session['quiz_' + quiz_name] = value

        return value
