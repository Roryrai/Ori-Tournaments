from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_optional
from app import db
from app.models import GroupName
from app.schemas import GroupNameSchema
from app.security import Security
from app.security import role_organizer


class GroupNameResource(Resource):
    schema = GroupNameSchema()
    list_schema = GroupNameSchema(many=True)

    # Queries group names
    def get(self):
        args = request.args
        if "id" in args and len(args) is not 1:
            return "'id' parameter may not be used with other parameters", 400
        group_name_id = args.get("id")
        name = args.get("name")
        sort = args.get("sort")
        reverse = args.get("reverse") == "true"

        if name:
            name = "%" name + "%"

        query = GroupName.query

        if group_name_id:
            query = query.filter(GroupName.id == group_name_id)

        if name:
            query = query.filter(GroupName.name.like(name))

        order = GroupName.name
        if sort == "id":
            order = GroupName.id
        if reverse:
            order = order.desc()
        query = query.order_by(order)
        group_names = query.all()

        return self.list_schema(group_names)

    # Creates a new group name. This is different from creating a new group.
    @role_organizer
    def post(self):
        data = request.get_json()
        group_name = self.schema.load(data)
        db.session.add(group_name)
        db.session.commit()
        return self.schema.dump(group_name), 201

    # Updates a group name. This just updates the name, not the runners
    @role_organizer
    def put(self):
        data = request.get_json()
        new = self.schema.load(data)
        existing = GroupName.query(new.id)
        if existing is not None:
            existing.group_name = new.group_name
            return
        else:
            abort(404)

    # Deletes a group name. This will, naturally, remove all runners from the group.
    # Currently not implemented while I decide if we even want this.
    def delete(self):
        abort(405)