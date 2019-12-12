from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_optional
from sqlalchemy import or_
from app import db

from app.models import User
from app.schemas import UserSchema
from app.auth import Auth

class UserResource(Resource):
    schema = UserSchema()
    list_schema = UserSchema(many=True)

    # Queries users based on request parameters
    def get(self):

        if "id" in request.args and len(request.args) is not 1:
            return "'id' parameter may not be used with other parameters", 400

        user_id = request.args.get("id")
        name = "%" + request.args.get("name") + "%" if "name" in request.args else None
        organizer = request.args.get("organizer") == "true"
        restream = request.args.get("restream") == "true"
        commentary = request.args.get("commentary") == "true"
        tracking = request.args.get("tracking") == "true"

        sort = request.args.get("sort")
        reverse = request.args.get("reverse") == "true"

        query = User.query
        # Get a user by user id
        if user_id:
            user = query.get(user_id)
            return self.list_schema.dump([user])

        # Find all users who match the filter conditions in the parameters.
        # Filters are AND except for name filters which are OR
        if name:
            filters = list()
            filters.append(User.username.like(name))
            filters.append(User.discord_name.like(name))
            filters.append(User.twitch_name.like(name))
            filters.append(User.srl_name.like(name))
            filters.append(User.src_name.like(name))
            query = query.filter(or_(*filters))
        if organizer:
            query = query.filter(User.organizer)
        if restream:
            query = query.filter(User.restream)
        if commentary:
            query = query.filter(User.commentary)
        if tracking:
            query = query.filter(User.tracking)

        users = query.all()

        # Default sort is alphabetical by username. May add other sorts later?
        if sort is None or sort == "name":
            users.sort(key=lambda x: x.username, reverse=reverse)
        elif sort == "id":
            users.sort(key=lambda x: x.id, reverse=reverse)
        return self.list_schema.dump(users)

    # Updates a user
    @jwt_required
    def put(self):
        data = request.get_json()
        new = self.schema.load(data)
        if new.id is not Auth.get_current_user().id:
            abort(401)
        existing = User.query.get(new.id)
        if existing is not None:
            db.session.delete(existing)
            db.session.add(new)
            db.session.commit()
            return
        else:
            abort(404)

    # Creates a new user. Must not be logged in.
    @jwt_optional
    def post(self):
        if Auth.get_current_user() is not None:
            abort(405)
        data = request.get_json()
        user = self.schema.load(data)
        db.session.add(user)
        db.session.commit()
        return self.schema.dump(user), 201

    # Deletes a user
    @Auth.role_organizer
    def delete(self):
        # if not Auth.get_current_user().is_organizer():
        #     abort(405)
        return "rest of method"
        user = User.query.get(request.args.get("id"))
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return
        else:
            abort(404)
