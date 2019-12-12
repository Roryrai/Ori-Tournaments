from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import User


class UserSchema(Schema):
    class Meta():
        ordered = True
    
    id = fields.Int()
    username = fields.Str()
    discord_name = fields.Str()
    pronunciation = fields.Str()
    pronouns = fields.Str()
    about = fields.Str()
    timestamp = fields.DateTime()
    is_organizer = fields.Bool()
    srl_name = fields.Str()
    twitch_name = fields.Str()
    src_name = fields.Str()
    input_method = fields.Str()
    restream = fields.Bool()
    commentary = fields.Bool()
    tracking = fields.Bool()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
