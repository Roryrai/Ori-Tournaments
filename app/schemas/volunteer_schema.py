from marshmallow import Schema, ValidationError
from marshmallow import fields
from marshmallow import post_load

from app.models import VolunteerInfo


class VolunteerSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    tournament_id = fields.Int()

    @post_load
    def make_runner_info(self, data, **kwargs):
        return VolunteerInfo(**data)

