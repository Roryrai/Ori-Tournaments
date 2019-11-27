from flask import request
from flask import abort
from flask_restful import Resource

from app import db
from app.models import Entrant
from app.schemas import EntrantSchema


class EntrantResource(Resource):
    schema = EntrantSchema()

    # Returns an entrant for a specific tournament if it exists
    def get(self):
        args = request.args
        tournament_id = args["tournament_id"]
        user_id = args["user_id"]
        entrant = Entrant.query.filter_by(tournament_id=tournament_id, user_id=user_id).first()
        if entrant:
            json = self.schema.dump(entrant)
            return json
        else:
            return None

    # Adds an entrant to a tournament (sign up for a tournament)
    def put(self):
        data = request.get_json()
        entrant = self.schema.load(data)
        db.session.add(entrant)
        db.session.commit()
        return self.schema.dump(entrant), 201

    # Deletes an entrant from a tournament (cancels registration)
    def delete(self):
        tournament_id = request.args["tournament_id"]
        user_id = request.args["user_id"]
        print(tournament_id, user_id)
        entrant = Entrant.query.filter_by(tournament_id=tournament_id, user_id=user_id).first()
        if entrant is not None:
            db.session.delete(entrant)
            db.session.commit()
            return
        else:
            abort(404)
