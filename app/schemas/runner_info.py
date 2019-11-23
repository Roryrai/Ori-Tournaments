from marshmallow import Schema
from marshmallow import fields


class RunnerInfoSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    srl_name = fields.Str()
    twitch_name = fields.Str()
    src_name = fields.Str()
    input_method = fields.Str()
