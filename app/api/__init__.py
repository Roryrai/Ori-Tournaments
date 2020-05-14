from flask import Blueprint
from flask_restful import Api

from .auth_resource import AuthResource
from .entrant_resource import EntrantResource
from .group_member_resource import GroupMemberResource
from .group_name_resource import GroupNameResource
# from .group_resource import GroupResource
from .question_resource import QuestionResource
from .race_resource import RaceResource
from .response_resource import ResponseResource
from .standings_resource import StandingsResource
from .tournament_resource import TournamentResource
from .volunteer_resource import VolunteerResource
from .user_resource import UserResource


bp = Blueprint("api", __name__)

api = Api(bp)

api.add_resource(AuthResource, "/auth")
api.add_resource(EntrantResource, "/entrant")
# api.add_resource(GroupResource, "/group")
api.add_resource(GroupMemberResource, "/group/member")
api.add_resource(GroupNameResource, "/group/name")
api.add_resource(QuestionResource, "/question")
api.add_resource(RaceResource, "/race")
api.add_resource(ResponseResource, "/response")
api.add_resource(StandingsResource, "/standings")
api.add_resource(TournamentResource, "/tournament")
api.add_resource(UserResource, "/user")
api.add_resource(VolunteerResource, "/volunteer")
