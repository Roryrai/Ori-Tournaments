from flask import abort
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import verify_jwt_in_request
from functools import wraps

from app.models import User


# Custom decorator that ensures a user is an organizer
@staticmethod
def role_organizer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user.is_organizer():
            abort(401)
        return fn(*args, **kwargs)

    return wrapper


class Security:
    # Returns the current user from the current jwt identity
    @staticmethod
    def get_current_user():
        user_id = get_jwt_identity()
        if not user_id:
            return None
        user = User.query.get(user_id)
        return user

    # Does the given user id match the current user id?
    @staticmethod
    def is_current_user(user_id):
        current_id = get_jwt_identity()
        return current_id == user_id

    # Does the given user id match the current user id, or is that user an admin?
    @staticmethod
    def is_current_user_or_organizer(user_id):
        current_id = get_jwt_identity()
        user = User.query.get(current_id)
        return user_id == current_id or user.is_organizer()