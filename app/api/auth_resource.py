from datetime import timedelta

from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from app.models import User


class AuthResource(Resource):
    def post(self):
        json = request.get_json()
        user = User.query.filter_by(username=json["username"]).first()
        if not user or not user.check_password(json["password"]):
            return "Invalid username or password", 401
        else:
            return {"access_token": create_access_token(identity=user.id, expires_delta=timedelta(days=1))}
