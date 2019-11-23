from flask import Blueprint
from app.api import user_resource

bp = Blueprint("api", __name__)

