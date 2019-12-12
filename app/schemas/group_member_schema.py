from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import GroupMember


class GroupMemberSchema(Schema):
    id = fields.Int()
    tournament_id = fields.Int()
    user_id = fields.Int()
    group_id = fields.Int()

    @post_load
    def make_group(self, data, **kwargs):
        return GroupMember(**data)