from datetime import datetime
from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_optional
from app import db
from app.models import Tournament
from app.schemas import TournamentSchema
from app.security import Security
from app.security import role_organizer


class TournamentResource(Resource):
    schema = TournamentSchema()
    list_schema = TournamentSchema(many=True)

    # Queries tournaments
    @jwt_optional
    def get(self):
        args = request.args
        if "id" in args and len(args) is not 1:
            return "'id' parameter may not be used with other parameters", 400
        tournament_id = args.get("id")
        name = args.get("name")
        if name:
            name = "%" + name + "%"
        category = args.get("category")
        if category:
            category = "%" + category + "%"
        hidden = args.get("hidden") == "true"
        active = args.get("active") == "true"

        sort = args.get("sort")
        reverse = args.get("reverse") == "true"

        query = Tournament.query

        # Get one by id
        if tournament_id:
            query = query.filter(Tournament.id == tournament_id)

        # Query on actual search parameters
        if name:
            query = query.filter(Tournament.name.like(name))
        if category:
            query = query.filter(Tournament.category.like(category))
        if not (Security.get_current_user() and Security.get_current_user().is_organizer()):
            query = query.filter(not Tournament.hidden)
        elif hidden:
            query = query.filter(Tournament.hidden)
        if active:
            query = query.filter(Tournament.active)

        # Sorting logic. Default sort is by id for now.
        order = Tournament.id
        if sort == "name":
            order = Tournament.name
        if sort == "category":
            order = Tournament.category
        if reverse:
            order = order.desc()
        query = query.order_by(order)
        tournaments = query.all()

        return self.list_schema.dump(tournaments)

    # Creates a tournament
    @role_organizer
    def post(self):
        data = request.get_json()
        tournament = self.schema.load(data)
        db.session.add(tournament)
        db.session.commit()
        return self.schema.dump(tournament), 201

    # Updates a tournament
    @role_organizer
    def put(self):
        data = request.get_json()
        new = self.schema.load(data)
        existing = Tournament.query.get(new.id)
        if existing is not None:
            existing.name = new.name
            existing.category = new.category
            existing.hidden = new.hidden
            existing.start_date = new.start_date
            existing.end_date = new.end_date
            existing.signups_open = new.signups_open
            existing.signups_close = new.signups_close
            existing.date_modified = datetime.utcnow
            db.session.commit()
            return
        else:
            abort(404)

    # Deletes a tournament
    @role_organizer
    def delete(self):
        tournament = Tournament.query.get(request.args.get("id"))
        if tournament is not None:
            db.session.delete(tournament)
            db.session.commit()
            return
        else:
            abort(404)
