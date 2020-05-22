"""
Забираем всю информацию из контейнеров и на её основе создаем таски в CTFd
"""
import os
from CTFd import create_app
from CTFd.utils.exports import import_ctf

import sys

app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db = app.db

        # Generating Challenges
        print("GENERATING CHALLENGES")
        print(os.listdir('../'))
        # for x in range(CHAL_AMOUNT):
        #     word = gen_word()
        #     chal = Challenges(
        #         name=word,
        #         description=gen_sentence(),
        #         value=gen_value(),
        #         category=gen_category(),
        #     )
        #     db.session.add(chal)
        #     db.session.commit()
        #     f = Flags(challenge_id=x + 1, content=word, type="static")
        #     db.session.add(f)
        #     db.session.commit()
        #
        # # Generating Files
        # print("GENERATING FILES")
        # AMT_CHALS_WITH_FILES = int(CHAL_AMOUNT * (3.0 / 4.0))
        # for x in range(AMT_CHALS_WITH_FILES):
        #     chal = random.randint(1, CHAL_AMOUNT)
        #     filename = gen_file()
        #     md5hash = hashlib.md5(filename.encode("utf-8")).hexdigest()
        #     chal_file = ChallengeFiles(
        #         challenge_id=chal, location=md5hash + "/" + filename
        #     )
        #     db.session.add(chal_file)
        #
        # db.session.commit()
        #
        # # Generating Teams
        # print("GENERATING TEAMS")
        # used = []
        # used_oauth_ids = []
        # count = 0
        # while count < TEAM_AMOUNT:
        #     name = gen_team_name()
        #     if name not in used:
        #         used.append(name)
        #         team = Teams(name=name, password="password")
        #         if random_chance():
        #             team.affiliation = gen_affiliation()
        #         if random_chance():
        #             oauth_id = random.randint(1, 1000)
        #             while oauth_id in used_oauth_ids:
        #                 oauth_id = random.randint(1, 1000)
        #             used_oauth_ids.append(oauth_id)
        #             team.oauth_id = oauth_id
        #         db.session.add(team)
        #         count += 1
        #
        # db.session.commit()
        #
        # # Generating Users
        # print("GENERATING USERS")
        # used = []
        # used_oauth_ids = []
        # count = 0
        # while count < USER_AMOUNT:
        #     name = gen_name()
        #     if name not in used:
        #         used.append(name)
        #         try:
        #             user = Users(name=name, email=gen_email(), password="password")
        #             user.verified = True
        #             if random_chance():
        #                 user.affiliation = gen_affiliation()
        #             if random_chance():
        #                 oauth_id = random.randint(1, 1000)
        #                 while oauth_id in used_oauth_ids:
        #                     oauth_id = random.randint(1, 1000)
        #                 used_oauth_ids.append(oauth_id)
        #                 user.oauth_id = oauth_id
        #             if mode == "teams":
        #                 user.team_id = random.randint(1, TEAM_AMOUNT)
        #             db.session.add(user)
        #             count += 1
        #         except Exception:
        #             pass
        #
        # db.session.commit()
        #
        # if mode == "teams":
        #     # Assign Team Captains
        #     print("GENERATING TEAM CAPTAINS")
        #     teams = Teams.query.all()
        #     for team in teams:
        #         captain = (
        #             Users.query.filter_by(team_id=team.id)
        #             .order_by(Users.id)
        #             .limit(1)
        #             .first()
        #         )
        #         if captain:
        #             team.captain_id = captain.id
        #     db.session.commit()
        #
        # # Generating Solves
        # print("GENERATING SOLVES")
        # if mode == "users":
        #     for x in range(USER_AMOUNT):
        #         used = []
        #         base_time = datetime.datetime.utcnow() + datetime.timedelta(
        #             minutes=-10000
        #         )
        #         for y in range(random.randint(1, CHAL_AMOUNT)):
        #             chalid = random.randint(1, CHAL_AMOUNT)
        #             if chalid not in used:
        #                 used.append(chalid)
        #                 user = Users.query.filter_by(id=x + 1).first()
        #                 solve = Solves(
        #                     user_id=user.id,
        #                     team_id=user.team_id,
        #                     challenge_id=chalid,
        #                     ip="127.0.0.1",
        #                     provided=gen_word(),
        #                 )
        #
        #                 new_base = random_date(
        #                     base_time,
        #                     base_time
        #                     + datetime.timedelta(minutes=random.randint(30, 60)),
        #                 )
        #                 solve.date = new_base
        #                 base_time = new_base
        #
        #                 db.session.add(solve)
        #                 db.session.commit()
        # elif mode == "teams":
        #     for x in range(1, TEAM_AMOUNT):
        #         used_teams = []
        #         used_users = []
        #         base_time = datetime.datetime.utcnow() + datetime.timedelta(
        #             minutes=-10000
        #         )
        #         team = Teams.query.filter_by(id=x).first()
        #         members_ids = [member.id for member in team.members]
        #         for y in range(random.randint(1, CHAL_AMOUNT)):
        #             chalid = random.randint(1, CHAL_AMOUNT)
        #             user_id = random.choice(members_ids)
        #             if (chalid, team.id) not in used_teams:
        #                 if (chalid, user_id) not in used_users:
        #                     solve = Solves(
        #                         user_id=user_id,
        #                         team_id=team.id,
        #                         challenge_id=chalid,
        #                         ip="127.0.0.1",
        #                         provided=gen_word(),
        #                     )
        #                     new_base = random_date(
        #                         base_time,
        #                         base_time
        #                         + datetime.timedelta(minutes=random.randint(30, 60)),
        #                     )
        #                     solve.date = new_base
        #                     base_time = new_base
        #                     db.session.add(solve)
        #                     db.session.commit()
        #                     used_teams.append((chalid, team.id))
        #                     used_users.append((chalid, user_id))
        #
        # db.session.commit()
        #
        # # Generating Awards
        # print("GENERATING AWARDS")
        # for x in range(USER_AMOUNT):
        #     base_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=-10000)
        #     for _ in range(random.randint(0, AWARDS_AMOUNT)):
        #         user = Users.query.filter_by(id=x + 1).first()
        #         award = Awards(
        #             user_id=user.id,
        #             team_id=user.team_id,
        #             name=gen_word(),
        #             value=random.randint(-10, 10),
        #             icon=gen_icon(),
        #         )
        #         new_base = random_date(
        #             base_time,
        #             base_time + datetime.timedelta(minutes=random.randint(30, 60)),
        #         )
        #         award.date = new_base
        #         base_time = new_base
        #
        #         db.session.add(award)
        #
        # db.session.commit()
        #
        # # Generating Wrong Flags
        # print("GENERATING WRONG FLAGS")
        # for x in range(USER_AMOUNT):
        #     used = []
        #     base_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=-10000)
        #     for y in range(random.randint(1, CHAL_AMOUNT * 20)):
        #         chalid = random.randint(1, CHAL_AMOUNT)
        #         if chalid not in used:
        #             used.append(chalid)
        #             user = Users.query.filter_by(id=x + 1).first()
        #             wrong = Fails(
        #                 user_id=user.id,
        #                 team_id=user.team_id,
        #                 challenge_id=chalid,
        #                 ip="127.0.0.1",
        #                 provided=gen_word(),
        #             )
        #
        #             new_base = random_date(
        #                 base_time,
        #                 base_time + datetime.timedelta(minutes=random.randint(30, 60)),
        #             )
        #             wrong.date = new_base
        #             base_time = new_base
        #
        #             db.session.add(wrong)
        #             db.session.commit()
        #
        # db.session.commit()
        # db.session.close()
        #
        # clear_config()
        # clear_standings()
        # clear_pages()


# app = create_app()
# with app.app_context():
#     import_ctf(sys.argv[1])
