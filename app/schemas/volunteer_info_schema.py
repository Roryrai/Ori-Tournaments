from marshmallow import Schema
from marshmallow import fields


class VolunteerInfoSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    restream = fields.Bool()
    commentary = fields.Bool()
    tracking = fields.Bool()
