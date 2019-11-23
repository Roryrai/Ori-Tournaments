from marshmallow import Schema
from marshmallow import fields


class GroupNameSchema(Schema):
    id = fields.Int()
    group_name = fields.Str()
