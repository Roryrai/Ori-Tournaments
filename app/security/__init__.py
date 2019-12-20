from flask import Blueprint
from .security import Security
from .security import role_organizer

bp = Blueprint("security", __name__)
