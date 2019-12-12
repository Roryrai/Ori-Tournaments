from flask import Blueprint
from .auth import authenticate
from .auth import identity

bp = Blueprint("auth", __name__)


