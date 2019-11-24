from flask import Blueprint
from .runner_info_schema import RunnerInfoSchema
from .volunteer_info_schema import VolunteerInfoSchema
from .user_schema import UserSchema
from .entrant_schema import EntrantSchema
from .race_schema import RaceSchema
from .race_result_schema import RaceResultSchema
from .response_schema import ResponseSchema
from .runner_group_schema import RunnerGroupSchema
from .tournament_schema import TournamentSchema
from .volunteer_schema import VolunteerSchema
from .group_name_schema import GroupNameSchema

bp = Blueprint("schemas", __name__)
