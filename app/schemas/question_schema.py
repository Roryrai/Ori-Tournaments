from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import Question


class QuestionSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    tournament_id = fields.Int()
    question = fields.Str()

    date_created = fields.Date()
    date_modified = fields.Date()

    @post_load
    def make_question(self, data, **kwargs):
        return Question(**data)
