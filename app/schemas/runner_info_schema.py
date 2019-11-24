from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import RunnerInfo


class RunnerInfoSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    srl_name = fields.Str()
    twitch_name = fields.Str()
    src_name = fields.Str()
    input_method = fields.Str()

    @post_load
    def make_runner_info(self, data, **kwargs):
        return RunnerInfo(**data)
