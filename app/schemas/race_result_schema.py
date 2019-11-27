from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import RaceResult


class RaceResultSchema(Schema):
    id = fields.Int()
    race_id = fields.Int()
    user_id = fields.Int()
    time = fields.TimeDelta()
    comments = fields.Str()

    @post_load
    def make_race_result(self, data, **kwargs):
        return RaceResult(**data)
