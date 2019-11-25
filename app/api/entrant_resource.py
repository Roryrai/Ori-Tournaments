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
        group_id = request.args["id"]
        entrant = Entrant.query.get(group_id)
        if entrant is not None:
            db.session.delete(entrant)
            db.session.commit()
            return
        else:
            abort(404)
