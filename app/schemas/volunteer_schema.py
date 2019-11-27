from marshmallow import Schema, ValidationError
from marshmallow import fields
from marshmallow import post_load


class VolunteerSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    tournament_id = fields.Int()

    @post_load
    def make_volunteer(self, data, **kwargs):
        return Volunteer(**data)

