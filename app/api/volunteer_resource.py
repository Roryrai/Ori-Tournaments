from flask import request
from flask import abort
from flask_restful import Resource

from app import db
from app.models import Volunteer
from app.schemas import VolunteerSchema

schema = VolunteerSchema()


class VolunteerResource(Resource):
    # Returns a volunteer for a specific tournament if it exists
    def get(self):
        args = request.args
        tournament_id = args["tournament_id"]
        user_id = args["user_id"]
        volunteer = Volunteer.query.filter_by(tournament_id=tournament_id, user_id=user_id).first()
        if volunteer:
            json = schema.dump(volunteer)
            return json
        else:
            return

    # Adds a volunteer to a tournament (sign up for a tournament)
    def put(self):
        data = request.get_json()
        volunteer = schema.load(data)
        db.session.add(volunteer)
        db.session.commit()
        return schema.dump(volunteer), 201

    # Deletes a volunteer from a tournament (cancels registration)
    def delete(self):
        tournament_id = request.args["tournament_id"]
        user_id = request.args["user_id"]
        print(tournament_id, user_id)
        volunteer = Volunteer.query.filter_by(tournament_id=tournament_id, user_id=user_id).first()
        if volunteer is not None:
            db.session.delete(volunteer)
            db.session.commit()
            return
        else:
            abort(404)
