from flask import Blueprint
from .user import UserSchema
from .runner_info import RunnerInfoSchema
from .volunteer_info import VolunteerInfoSchema
from .entrant import EntrantSchema
from .race import RaceSchema
from .race_result import RaceResultSchema
from .response import ResponseSchema
from .runner_group import RunnerGroupSchema
from .tournament import TournamentSchema
from .volunteer import VolunteerSchema

bp = Blueprint("schemas", __name__)
