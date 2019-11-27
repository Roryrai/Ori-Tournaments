from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import Race

class RaceSchema(Schema):
    id = fields.Int()
    date = fields.Date()
    number_entrants = fields.Int()
    tournament_id = fields.Int()
    bracket_id = fields.Int()
    comments = fields.Str()

    @post_load
    def make_race(self, data, **kwargs):
        return Race(**data)
