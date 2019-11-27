from flask_restful import Resource

from app.models import User
from app.schemas import UserSchema

schema = UserSchema()


class UsersResource(Resource):
    # Returns a list of all users
    def get(self):
        users = User.query.all()
        user_schema = UserSchema(many=True)
        return user_schema.dump(users)
