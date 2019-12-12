from flask import Blueprint
from flask_restful import Api
from .user_resource import UserResource
from .group_resource import GroupResource
from .group_member_resource import GroupMemberResource
from .group_name_resource import GroupNameResource
from .group_names_resource import GroupNamesResource
from .entrant_resource import EntrantResource
from .entrants_resource import EntrantsResource
from .volunteer_resource import VolunteerResource
from .volunteers_resource import VolunteersResource
from .tournament_resource import TournamentResource
from .tournaments_resource import TournamentsResource

from .auth_resource import AuthResource

bp = Blueprint("api", __name__)

api = Api(bp)

api.add_resource(UserResource, "/user")
api.add_resource(GroupResource, "/group")
api.add_resource(GroupMemberResource, "/groupmember")
api.add_resource(GroupNameResource, "/groupname")
api.add_resource(GroupNamesResource, "/groupnames")
api.add_resource(EntrantResource, "/entrant")
api.add_resource(EntrantsResource, "/entrants")
api.add_resource(VolunteerResource, "/volunteer")
api.add_resource(VolunteersResource, "/volunteers")
api.add_resource(TournamentResource, "/tournament")
api.add_resource(TournamentsResource, "/tournaments")

api.add_resource(AuthResource, "/auth")