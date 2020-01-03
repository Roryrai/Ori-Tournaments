from flask import Blueprint
from .user_schema import UserSchema
from .entrant_schema import EntrantSchema
from .race_result_schema import RaceResultSchema

from .race_schema import RaceSchema
from .response_schema import ResponseSchema
from .group_member_schema import GroupMemberSchema
from .tournament_schema import TournamentSchema
from .volunteer_schema import VolunteerSchema
from .group_name_schema import GroupNameSchema

bp = Blueprint("schemas", __name__)
