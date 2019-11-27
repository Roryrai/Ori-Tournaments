from flask import request
from flask import abort
from flask_restful import Resource

from app import db
from app.models import GroupName
from app.schemas import GroupNameSchema


class GroupNameResource(Resource):
    schema = GroupNameSchema()

    # Get a group name
    def get(self):
        group_name = GroupName.query.get(request.args["id"])
        json = self.schema.dump(group_name)
        return json

    # Update a group name
    def post(self):
        data = request.get_json()
        new = self.schema.load(data)
        existing = GroupName.query.get(new.id)
        if existing is not None:
            db.session.delete(existing)
            db.session.add(new)
            db.session.commit()
            return
        else:
            abort(404)

    # Create a group name
    def put(self):
        data = request.get_json()
        group_name = self.schema.load(data)
        db.session.add(group_name)
        db.session.commit()
        return self.schema.dump(group_name), 201

    # Delete a group name
    def delete(self):
        group_name = GroupName.query.get(request.args["id"])
        if group_name is not None:
            db.session.delete(group_name)
            db.session.commit()
            return
        else:
            abort(404)
