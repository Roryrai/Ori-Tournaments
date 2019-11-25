from flask import request
from flask import abort
from flask_restful import Resource

from app import db
from app.models import GroupName
from app.schemas import GroupNameSchema

schema = GroupNameSchema()


class GroupNameResource(Resource):
    def get(self):
        args = request.args
        group_id = args["id"]
        group_name = GroupName.query.get(group_id)
        json = schema.dump(group_name)
        return json

    def post(self):
        data = request.get_json()
        new = schema.load(data)
        existing = GroupName.query.get(new.id)
        if existing is not None:
            db.session.delete(existing)
            db.session.add(new)
            db.session.commit()
            return
        else:
            abort(404)

    def put(self):
        data = request.get_json()
        group_name = schema.load(data)
        db.session.add(group_name)
        db.session.commit()
        return schema.dump(group_name), 201

    def delete(self):
        group_id = request.args["id"]
        group_name = GroupName.query.get(group_id)
        if group_name is not None:
            db.session.delete(group_name)
            db.session.commit()
            return
        else:
            abort(404)
