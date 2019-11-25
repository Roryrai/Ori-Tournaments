from flask import Blueprint
from .user_resource import UserResource
from .group_name_resource import GroupNameResource
from .entrant_resource import EntrantResource
from .entrants_resource import EntrantsResource

bp = Blueprint("api", __name__)

