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
        if not (Security.get_current_user() and Security.get_current_user().is_organizer()) and hidden:
            query = query.filter(Tournament.visible)
        elif hidden:
            query = query.filter(Tournament.visible)
        if active:
            query = query.filter(Tournament.active)

        tournaments = query.all()

        # Default sort is by id for now. Should probably be by something else.
        if sort is None or sort == "id":
            tournaments.sort(key=lambda x: x.id, reverse=reverse)
        elif sort == "name":
            tournaments.sort(key=lambda x: x.id, reverse=reverse)
        return self.list_schema.dump(tournaments)

    # Creates a tournament
    @role_organizer
    def post(self):
        data = request.get_json()
        tournament = self.load(data)
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
            db.session.delete(existing)
            db.session.add(new)
            db.session.commit()
            return
        else:
            abort(404)

    # Deletes a tournament
    @role_organizer
    def delete(self):
        tournament = Tournament.query.get(request.args["id"])
        if tournament is not None:
            db.session.delete(tournament)
            db.session.commit()
            return
        else:
            abort(404)
