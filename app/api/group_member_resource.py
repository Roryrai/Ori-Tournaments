from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import GroupMember
from app.models import User
from app.schemas import GroupMemberSchema
from app.schemas import UserSchema
from app.security import Security

class GroupMemberResource(Resource):
    schema = GroupMemberSchema(many=True)

    def get(self):
        args = request.args
        tournament_id = args.get("tournament_id")
        group_id = args.get("group_id")
        user_id = args.get("user_id")

        res = GroupMemberService.query_all(tournament_id, group_id, user_id)
        if len(res) == 0:
            abort(404)
        return schema.dump(res)


    def post(self):
        data = request.get_json()
        