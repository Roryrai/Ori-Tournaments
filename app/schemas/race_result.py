from marshmallow import Schema
from marshmallow import fields


class RaceResultSchema(Schema):
    id = fields.Int()
    race_id = fields.Int()
    user_id = fields.Int()
    time = fields.TimeDelta()
    comments = fields.Str()
