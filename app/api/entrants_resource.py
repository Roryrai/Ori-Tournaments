from flask import request
from flask import abort
from flask_restful import Resource

from app import db
from app.models import Entrant
from app.models import User
from app.schemas import EntrantSchema
from app.schemas import UserSchema

schema = EntrantSchema()


class EntrantsResource(Resource):
    def get(self):
        args = request.args
        tournament_id = args["tournament_id"]
        entrants = db.session.query(User).join(User.tournaments_entered).\
            filter(Entrant.tournament_id == tournament_id).all()
        user_schema = UserSchema(many=True)

        res = user_schema.dump(entrants)
        return res

    # def put(self):
    #     data = request.get_json()
    #     entrant = schema.load(data)
    #     db.session.add(entrant)
    #     db.session.commit()
    #     return schema.dump(entrant), 201
    #
    # def delete(self):
    #     tournament_id = request.args["tournament_id"]
    #     user_id = request.args["user_id"]
    #     print(tournament_id, user_id)
    #     entrant = Entrant.query.filter_by(tournament_id=tournament_id, user_id=user_id).first()
    #     if entrant is not None:
    #         db.session.delete(entrant)
    #         db.session.commit()
    #         return
    #     else:
    #         abort(404)
