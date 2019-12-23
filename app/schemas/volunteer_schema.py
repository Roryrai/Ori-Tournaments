from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import Volunteer


class VolunteerSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    user_id = fields.Int()
    tournament_id = fields.Int()

    @post_load
    def make_volunteer(self, data, **kwargs):
        return Volunteer(**data)
