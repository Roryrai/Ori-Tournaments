from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_optional
from sqlalchemy import exc
from sqlalchemy import or_
from app import db

from app.models import User
from app.schemas import UserSchema
from app.security import Security
from app.security import role_organizer


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
        password = data["password"]
        print(password)
        try:
            del data["password"]
        except KeyError:
            abort(400)
        user = self.schema.load(data)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            return "That username is taken", 500
        return self.schema.dump(user), 201

    # Updates a user
    @jwt_required
    def put(self):
        data = request.get_json()
        new = self.schema.load(data)
        if new.id is not Security.get_current_user().id:
            abort(401)
        existing = User.query.get(new.id)
        if existing is not None:
            existing.username = new.username
            existing.discord_name = new.discord_name
            existing.pronunciation = new.pronunciation
            existing.pronouns = new.pronouns
            existing.about = new.about
            existing.sql_name = new.srl_name
            existing.twitch_name = new.twitch_name
            existing.src_name = new.src_name
            existing.input_method = new.input_method
            existing.restream = new.restream
            existing.commentary = new.commentary
            existing.tracking = new.tracking
            existing.date_modified = datetime.utcnow()
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
