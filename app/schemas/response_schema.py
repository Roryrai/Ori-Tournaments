from marshmallow import Schema
from marshmallow import fields


class ResponseSchema(Schema):
    id = fields.Int()
    question_id = fields.Int()
    user_id = fields.Int()
