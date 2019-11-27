from flask import request
from flask import abort
from flask_restful import Resource

from app import db

from app.models import User
from app.schemas import UserSchema


class UserResource(Resource):
    schema = UserSchema()

    # Retrieves a user
    def get(self):
        user = User.query.get(request.args["id"])
        json = self.schema.dump(user)
        return json

    # Updates a user
    def post(self):
        data = request.get_json()
        new = self.schema.load(data)
        existing = User.query.get(new.id)
        if existing is not None:
            db.session.delete(existing)
            db.session.add(new)
            return
        else:
            abort(404)

    # Creates a new user
    def put(self):
        data = request.get_json()
        user = self.schema.load(data)
        db.session.add(user)
        db.session.commit()
        return self.schema.dump(user), 201

    # Deletes a user
    def delete(self):
        user = User.query.get(request.args["id"])
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return
        else:
            abort(404)