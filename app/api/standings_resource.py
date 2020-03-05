from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from app.models import User
from app.models import Tournament
from app.models import QualifierStandings
from app.schemas import GroupStandingsSchema
from app.schemas import QualifierStandingsSchema
from app.schemas import UserSchema
from app.services import StandingsService
from app.security import Security
from app.security import role_organizer

from datetime import datetime

class StandingsResource(Resource):
    qualifier_schema = QualifierStandingsSchema(many=True)
    group_schema = GroupStandingsSchema(many=True)

    def get(self):
        args = request.args
        if "tournament_id" in request.args:
            id = args.get("tournament_id")
            tournament = Tournament.query.get(id)
            if not Tournament:
                return "Unable to find tournament", 404
            if tournament.format == Tournament.group_format:
                standings = StandingsService.getGroupStandings(tournament)
                return self.group_schema.dump(standings)
            elif tournament.format == Tournament.qualifier_format:
                standings = StandingsService.getQualifierStandings(tournament)
                return self.qualifier_schema.dump(standings)


