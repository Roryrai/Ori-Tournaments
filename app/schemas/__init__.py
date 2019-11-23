from flask import Blueprint
from .user import UserSchema
from .runner_info import RunnerInfoSchema
from .volunteer_info import VolunteerInfoSchema

bp = Blueprint("schemas", __name__)
