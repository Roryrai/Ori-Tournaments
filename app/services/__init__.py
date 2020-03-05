from flask import Blueprint

from .standings_service import StandingsService

bp = Blueprint("standings", __name__)
