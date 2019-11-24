from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.models import User
from app.schemas import UserSchema


class UserResource(Resource):
    def get(self):
        args = request.args
        user_id = args["user_id"]
        user = User.query.get(user_id)
        schema = UserSchema()
        json = schema.dump(user)
        return json

    def post(self, user):
        pass

    def put(self):
        schema = UserSchema()
        user_data = request.get_json()
        print(user_data)
        schema.load(user_data)
        return
