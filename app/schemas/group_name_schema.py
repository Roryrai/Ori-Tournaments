from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import GroupName


class GroupNameSchema(Schema):
    id = fields.Int()
    group_name = fields.Str()

    @post_load
    def make_group_name(self, data, **kwargs):
        return GroupName(**data)