from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import GroupMember
from app.models import User
from app.models import GroupName


class GroupMemberSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    tournament_id = fields.Int()
    runner = fields.Pluck(UserSchema, "username", attribute=user)
    group_name= fields.Pluck(GroupNameSchema, "group_name", attribute="group")

    @post_load
    def make_group(self, data, **kwargs):
        return GroupMember(**data)
