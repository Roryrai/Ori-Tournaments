from flask_restful import Resource

from app.models import Tournament
from app.schemas import TournamentSchema


class TournamentsResource(Resource):
    schema = TournamentSchema(many=True)

    # Returns a list of all tournaments
    def get(self):
        tournaments = Tournament.query.all()
        return self.schema.dump(tournaments)
