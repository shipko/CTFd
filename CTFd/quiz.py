from flask import render_template, Blueprint
from CTFd.utils.decorators import (
    during_ctf_time_only,
    require_verified_emails,
    require_team,
)
from CTFd.utils.decorators.visibility import check_challenge_visibility
from CTFd.utils import config, get_config
from CTFd.utils.dates import ctf_ended, ctf_paused, view_after_ctf
from CTFd.utils.helpers import get_errors, get_infos

quiz = Blueprint("quiz", __name__)


@quiz.route("/quiz/<int:quiz_id>", methods=["GET"])
@during_ctf_time_only
@require_verified_emails
@check_challenge_visibility
@require_team
def listing(quiz_id):
    quiz = {
        'count': 20
    }
    return render_template(
        "quiz-plugin/quiz.html", quiz = quiz
    )
