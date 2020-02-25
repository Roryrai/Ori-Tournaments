from flask import Blueprint
from flask_restful import Api

from .auth_resource import AuthResource
from .entrant_resource import EntrantResource
from .question_resource import QuestionResource
from .race_resource import RaceResource
from .response_resource import ResponseResource
from .tournament_resource import TournamentResource
from .volunteer_resource import VolunteerResource
from .user_resource import UserResource


bp = Blueprint("api", __name__)

api = Api(bp)

api.add_resource(AuthResource, "/auth")
api.add_resource(EntrantResource, "/entrant")
api.add_resource(QuestionResource, "/question")
api.add_resource(RaceResource, "/race")
api.add_resource(ResponseResource, "/response")
api.add_resource(TournamentResource, "/tournament")
api.add_resource(UserResource, "/user")
api.add_resource(VolunteerResource, "/volunteer")
