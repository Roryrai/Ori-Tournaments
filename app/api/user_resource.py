from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from app import db

from app.models import User
from app.schemas import UserSchema
from app.security import Security
from app.security import role_organizer

from datetime import datetime

class UserResource(Resource):
    schema = UserSchema()
    list_schema = UserSchema(many=True)

    # Queries users based on request parameters
    def get(self):
        args = request.args
        if "id" in args and len(args) is not 1:
            return "'id' parameter may not be used with other parameters", 400

        user_id = args.get("id")
        name = args.get("name")
        if name:
            name = "%" + name + "%"
        organizer = args.get("organizer") == "true"
        restream = args.get("restream") == "true"
        commentary = args.get("commentary") == "true"
        tracking = args.get("tracking") == "true"

        sort = args.get("sort")
        reverse = args.get("reverse") == "true"

        query = User.query
        # Get a user by user id. If this is present no other args are present.
        if user_id:
            query = query.filter(User.id == user_id)

        # Find all users who match the filter conditions in the parameters.
        # Filters are AND except for name filters which are OR
        if name:
            filters = list()
            filters.append(User.username.ilike(name))
            filters.append(User.discord_name.ilike(name))
            filters.append(User.twitch_name.ilike(name))
            filters.append(User.srl_name.ilike(name))
            filters.append(User.src_name.ilike(name))
            query = query.filter(or_(*filters))
        if organizer:
            query = query.filter(User.organizer)
        if restream:
            query = query.filter(User.restream)
        if commentary:
            query = query.filter(User.commentary)
        if tracking:
            query = query.filter(User.tracking)

        # Sorting logic. Default sort is alphabetical by username. Can also sort by user id right now.
        order = User.username
        if sort == "id":
            order = User.id
        if reverse:
            order = order.desc()
        query = query.order_by(order)
        users = query.all()

        return self.list_schema.dump(users)

    # Creates a new user. Must not be logged in.
    @jwt_optional
    def post(self):
        if Security.get_current_user() is not None:
            abort(405)
        data = request.get_json()
        user_data = data["user"]
        user = self.schema.load(user_data)
        user.set_password(data["password"])
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "That username is taken", 500
        return self.schema.dump(user), 201

    # Updates a user
    @jwt_required
    def put(self):
        data = request.get_json()
        user_data = data["user"]
        new_data = self.schema.load(user_data)
        current_id = Security.get_current_user().id
        if new_data.id is not current_id:
            abort(401)
        user = User.query.get(current_id)
        if user is not None:
            if "password" in data.keys():
                if "old_password" in data.keys() and user.check_password(data["old_password"]):
                    user.set_password(data["password"])
                else:
                    return "Current password is incorrect", 401
            user.username = new_data.username
            user.discord_name = new_data.discord_name
            user.pronunciation = new_data.pronunciation
            user.pronouns = new_data.pronouns
            user.about = new_data.about
            user.sql_name = new_data.srl_name
            user.twitch_name = new_data.twitch_name
            user.src_name = new_data.src_name
            user.input_method = new_data.input_method
            user.restream = new_data.restream
            user.commentary = new_data.commentary
            user.tracking = new_data.tracking
            user.date_modified = datetime.utcnow()
            db.session.commit()
            return
        else:
            abort(404)

    # Deletes a user
    @role_organizer
    def delete(self):
        user = User.query.get(request.args.get("id"))
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return
        else:
            abort(404)
