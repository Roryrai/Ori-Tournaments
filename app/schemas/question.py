from marshmallow import Schema
from marshmallow import fields


class QuestionSchema(Schema):
    id = fields.Int()
    tournament_id = fields.Int()
    question = fields.Str()
