from flask_restful import Resource
from app.models import User


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        return {"user": user.username}
