from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import Tournament


class TournamentSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    category = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    signups_open = fields.Date()
    signups_close = fields.Date()
    hidden = fields.Bool()
    name = fields.Str()
    active = fields.Bool()

    registration_open = fields.Bool()

    @post_load
    def make_tournament(self, data, **kwargs):
        return Tournament(**data)
