from marshmallow import Schema
from marshmallow import fields

from app.schemas.runner_info import RunnerInfoSchema
from app.schemas.volunteer_info import VolunteerInfoSchema


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