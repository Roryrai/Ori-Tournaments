from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Entrant
from app.models import User
from app.schemas import UserSchema
from app.security import Security


class EntrantResource(Resource):
    schema = UserSchema(many=True)

    # Queries entrants based on user id and tournament id
    def get(self):
        args = request.args
        tournament_id = args.get("tournament_id")

        # Build query
        query = db.session.query(User).join(User.tournaments_entered)

        if tournament_id:
            query = query.filter(Entrant.tournament_id == tournament_id)

        entrants = query.all()
        return self.schema.dump(entrants)

    # Adds an entrant to a tournament (sign up for a tournament)
    @jwt_required
    def post(self):
        data = request.get_json()
        try:
            entrant = Entrant(tournament_id=data.get("tournament_id"),
                          user_id=Security.get_current_user().id)
            db.session.add(entrant)
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
        entrant = Entrant.query.filter_by(tournament_id=tournament_id, user_id=user_id).first()
        if entrant is not None:
            db.session.delete(entrant)
            db.session.commit()
            return
        else:
            abort(404)
