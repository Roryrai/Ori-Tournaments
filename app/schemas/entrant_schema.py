from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import Entrant


class EntrantSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    tournament_id = fields.Int()

    @post_load
    def make_entrant(self, data, **kwargs):
        return Entrant(**data)
