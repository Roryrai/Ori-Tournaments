
from app import db

from app.models import Tournament
from app.models import Entrant
from app.models import GroupMember
from app.models import User


class GroupMemberService():

    def randomize(tournament_id):
        tournament = Tournament.query.get(tournament_id)

        for entrant in tournament.entrants:
            pass


    # Takes a list of user ids to add to the group
    def add_group(user_ids, group_id, tournament_id):

        for user_id in user_ids:
            group_member = GroupMember(user_id=user_id, group_id=group_id, tournament_id=tournament_id)
            db.session.add(group_member)
            db.session.commit()
