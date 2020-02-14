from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import RaceResult
from app.schemas import UserSchema


class RaceResultSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    race_id = fields.Int()
    runner = fields.Pluck(UserSchema, "username", attribute="user")
    time = fields.TimeDelta()
    comments = fields.Str()

    @post_load
    def make_race_result(self, data, **kwargs):
        return RaceResult(**data)
