from flask import request
from flask_restful import Resource

from app import db
from app.models import Volunteer
from app.models import User
from app.schemas import UserSchema


class VolunteersResource(Resource):
    schema = UserSchema(many=True)

    # Returns a list of volunteers for a tournament
    def get(self):
        args = request.args
        tournament_id = args["tournament_id"]
        volunteers = db.session.query(User).join(User.tournaments_volunteered).\
            filter(Volunteer.tournament_id == tournament_id).all()

        res = self.schema.dump(volunteers)
        return res
