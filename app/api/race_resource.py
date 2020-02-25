from datetime import datetime
from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_optional
from sqlalchemy import Date
from sqlalchemy import cast
# from sqlalchemy import _in

from app import db
from app.models import Race
from app.models import RaceResult
from app.schemas import RaceSchema
from app.schemas import RaceResultSchema
from app.security import Security
from app.security import role_organizer


class RaceResource(Resource):
    schema = RaceSchema()
    list_schema = RaceSchema(many=True)

    @jwt_optional
    def get(self):
        args = request.args
        if "id" in args and len(args) is not 1:
            return "'id' parameter may not be used with other parameters", 400
        race_id = args.get("id")

        date = args.get("date")
        tournament_id = args.get("tournament_id")
        bracket_id = args.get("bracket_id")
        runners = args.get("runner").split(",")
        print(runners)
        sort = args.get("sort")
        reverse = args.get("reverse") == "true"

        query = db.session.query(Race).join(Race.results)

        # Get one by id
        if race_id:
            query = query.filter(Race.id == race_id)

        # Build query from search params
        if tournament_id:
            query = query.filter(Race.tournament_id == tournament_id)
        if bracket_id:
            query = query.filter(Race.bracket_id == bracket_id)
        if date:
            query = query.filter(cast(Race.date, Date) == date)
        if runners:
            for runner in runners:
                query = query.filter(RaceResult.user_id.in_(runner))

        # Sorting logic Default sort by date desc
        order = Race.date.desc()
        if sort == "date":
            order = Race.date
        if sort == "bracket_id":
            order = Race.bracket_id
        if reverse:
            order = order.desc()
        query = query.order_by(order)

        print(str(query))
        races = query.all()
        return self.list_schema.dump(races)

    # Create a race
    @role_organizer
    def post(self):
        data = request.get_json()
        race = self.schema.load(data)
        db.session.add(race)
        db.session.commit()
        return self.schema.dump(race), 201

    @role_organizer
    def put(self):
        data = request.get_json()
        new = self.schema.load(data)
        existing = Race.query.get(new.id)
        if existing is not None:
            # existing.date = new.date
            existing.number_entrants = new.number_entrants
            existing.tournament_id = new.tournament_id
            existing.bracket_id = new.bracket_id
            existing.comments = new.comments
            existing.date_modified = datetime.utcnow
            db.session.commit()

    @role_organizer
    def delete(self):
        race = Race.query.get(request.args.get("id"))
        if race is not None:
            db.session.delete(race)
            db.session.commit()
            return
        else:
            abort(404)
