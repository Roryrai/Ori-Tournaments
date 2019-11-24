from marshmallow import Schema
from marshmallow import fields


class RaceSchema(Schema):
    id = fields.Int()
    date = fields.Date()
    number_entrants = fields.Int()
    tournament_id = fields.Int()
    bracket_id = fields.Int()
    comments = fields.Str()
