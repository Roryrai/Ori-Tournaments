from flask import request
from flask_restful import Resource

from app import db
from app.models import Entrant
from app.models import User
from app.schemas import UserSchema


class EntrantsResource(Resource):
    schema = UserSchema(many=True)

    # Returns a list of entrants for a given tournament
    def get(self):
        args = request.args
        tournament_id = args["tournament_id"]
        entrants = db.session.query(User).join(User.tournaments_entered).\
            filter(Entrant.tournament_id == tournament_id).all()

        res = self.schema.dump(entrants)
        return res
