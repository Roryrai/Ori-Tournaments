from flask import request
from flask_restful import Resource

from app import db
from app.models import GroupMember
from app.models import User
from app.schemas import GroupMemberSchema
from app.schemas import UserSchema


class GroupMemberResource(Resource):
    user_schema = UserSchema()
    group_member_schema = GroupMemberSchema()

    # Returns a list of runners in the given group. Does not contain standings info.
    def get(self):
        tournament_id = request.args["tournament_id"]
        user_id = request.args["user_id"]
        group_member = db.session.query(User).join(User.groups).\
            filter(GroupMember.tournament_id == tournament_id,
                   GroupMember.user_id == user_id).first()
        if group_member:
            return self.user_schema.dump(group_member)
        else:
            return None

    # Adds a member to a group
    def put(self):
        data = request.get_json()
        group_member = self.group_member_schema.load(data)
        db.session.add(group_member)
        db.session.commit()
        return None, 201

    # Remove a runner from a group
    def delete(self):
        data = request.get_json()
        group_member = self.group_member_schema.load()
        db.session.delete(group_member)
        db.session.commit()