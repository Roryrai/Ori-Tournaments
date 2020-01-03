from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import Race
from app.schemas import RaceResultSchema


class RaceSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    date = fields.Date()
    number_entrants = fields.Int()
    tournament_id = fields.Int()
    bracket_id = fields.Int()
    comments = fields.Str()
    results = fields.Nested(RaceResultSchema(many=True, only=("user_id", "time",)))

    @post_load
    def make_race(self, data, **kwargs):
        return Race(**data)
