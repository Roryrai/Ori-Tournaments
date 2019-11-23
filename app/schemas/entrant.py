from marshmallow import Schema
from marshmallow import fields


class EntrantSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    tournament_id = fields.Int()
