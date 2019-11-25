from flask import request
from flask import abort
from flask_restful import Resource

from app import db
from app.models import Entrant
from app.schemas import EntrantSchema

schema = EntrantSchema()


class EntrantResource(Resource):
    def get(self):
        args = request.args
        entrant_id = args["id"]
        entrant = Entrant.query.get(entrant_id)
        json = schema.dump(entrant)
        return json

    def put(self):
        data = request.get_json()
        entrant = schema.load(data)
        db.session.add(entrant)
        db.session.commit()
        return schema.dump(entrant), 201

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
