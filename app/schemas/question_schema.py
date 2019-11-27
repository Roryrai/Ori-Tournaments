from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load


class QuestionSchema(Schema):
    id = fields.Int()
    tournament_id = fields.Int()
    question = fields.Str()
