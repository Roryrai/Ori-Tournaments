from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Volunteer
from app.models import User
from app.schemas import UserSchema
from app.security import Security


class VolunteerResource(Resource):
    schema = UserSchema(many=True)

    # Returns a volunteer for a specific tournament if it exists
    def get(self):
        args = request.args
        tournament_id = args.get("tournament_id")

        # Build query
        query = db.session.query(User).join(User.tournaments_volunteered)

        if tournament_id:
            query = query.filter(Volunteer.tournament_id == tournament_id)

        volunteers = query.all()
        return self.schema.dump(volunteers)

    # Adds a volunteer to a tournament (sign up for a tournament)
    @jwt_required
    def post(self):
        data = request.get_json()
        try:
            volunteer = Volunteer(tournament_id=data.get("tournament_id"), \
                                user_id=Security.get_current_user().id)
            db.session.add(volunteer)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "You've already signed up for this event"
        return None, 201

    # Deletes an entrant from a tournament (cancels registration)
    @jwt_required
    def delete(self):
        tournament_id = request.args.get("tournament_id")
        user_id = request.args.get("user_id")
        if user_id is None:
            user_id = Security.get_current_user().id
        if not Security.is_current_user_or_organizer(user_id):
            abort(401)
        volunteer = Volunteer.query.filter_by(tournament_id=tournament_id, user_id=user_id).first()
        if volunteer is not None:
            db.session.delete(volunteer)
            db.session.commit()
            return
        else:
            abort(404)
