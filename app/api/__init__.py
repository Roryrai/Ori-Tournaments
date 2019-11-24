from flask import Blueprint
from .user_resource import UserResource
from .group_name_resource import GroupNameResource

bp = Blueprint("api", __name__)

