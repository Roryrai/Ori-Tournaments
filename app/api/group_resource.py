from flask import request
from flask_restful import Resource

from app import db
from app.models import Group
from app.models import User
from app.schemas import GroupSchema
from app.schemas import UserSchema


class GroupResource(Resource):
    schema = GroupSchema(many=True)

    # Returns a list of runners in the given group. Does not contain standings info.
    def get(self):
        group_id = request.args["group_id"]
        tournament_id = request.args["tournament_id"]
        group_members = db.session.query(User).join(User.groups).\
            filter(Group.tournament_id == tournament_id, Group.group_id == group_id).all()
        if group_members:
            user_schema = UserSchema(many=True)
            return user_schema.dump(group_members)
        else:
            return None

