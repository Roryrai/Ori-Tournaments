from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import Response


class ResponseSchema(Schema):
    id = fields.Int()
    question_id = fields.Int()
    user_id = fields.Int()

    @post_load
    def make_response(self, data, **kwargs):
        return Response(**data)
