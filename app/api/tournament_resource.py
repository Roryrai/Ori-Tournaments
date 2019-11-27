from flask import request
from flask import abort
from flask_restful import Resource

from app import db
from app.models import Tournament
from app.schemas import TournamentSchema


class TournamentResource(Resource):
    schema = TournamentSchema()

    # Returns a tournament
    def get(self):
        tournament = Tournament.query.get(request.args["id"])
        json = self.schema.dump(tournament)
        return json

    # Updates a tournament
    def post(self):
        data = request.get_json()
        new = self.schema.load(data)
        existing = Tournament.query.get(new.id)
        if existing is not None:
            db.session.delete(existing)
            db.session.add(new)
            db.session.commit()
            return
        else:
            abort(404)

    # Creates a tournament
    def put(self):
        data = request.get_json()
        tournament = self.load(data)
        db.session.add(tournament)
        db.session.commit()
        return self.schema.dump(tournament), 201

    # Deletes a tournament
    def delete(self):
        tournament = Tournament.query.get(request.args["id"])
        if tournament is not None:
            db.session.delete(tournament)
            db.session.commit()
            return
        else:
            abort(404)
