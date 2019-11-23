from flask_restful import Resource
from app.models import User, UserSchema


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        schema = UserSchema()
        json = schema.dump(user)
        return json

    def post(self, user):
        pass
