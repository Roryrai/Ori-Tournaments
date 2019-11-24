from marshmallow import Schema
from marshmallow import fields


class RunnerGroupSchema(Schema):
    id = fields.Int()
    tournament_id = fields.Int()
    user_id = fields.Int()
    group_id = fields.Int()
