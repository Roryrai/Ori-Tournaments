from flask import abort
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import verify_jwt_in_request
from functools import wraps

from app.models import User


class Auth:
    def get_current_user():
        user_id = get_jwt_identity()
        if not user_id:
            return None
        user = User.query.get(user_id)
        return user

    # Custom decorator that ensures a user is logged in
    def login_required(fn):
        pass

    # Custom decorator that ensures a user is an organizer
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
