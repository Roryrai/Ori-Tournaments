from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import User, RunnerInfo, VolunteerInfo
from app.schemas import RunnerInfoSchema
from app.schemas import VolunteerInfoSchema


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    discord_name = fields.Str()
    pronunciation = fields.Str()
    pronouns = fields.Str()
    about = fields.Str()
    timestamp = fields.DateTime()
    is_organizer = fields.Bool()
    runner_info = fields.Nested(RunnerInfoSchema)
    volunteer_info = fields.Nested(VolunteerInfoSchema)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
