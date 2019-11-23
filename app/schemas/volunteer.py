from marshmallow import Schema
from marshmallow import fields


class VolunteerSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    tournament_id = fields.Int()