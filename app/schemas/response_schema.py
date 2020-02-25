from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import Response
from app.schemas import QuestionSchema
from app.schemas import UserSchema

class ResponseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    question_id = fields.Int()
    user_id = fields.Int()

    username = fields.Pluck(UserSchema, "username", attribute="user")
    question = fields.Pluck(QuestionSchema, "question", attribute="question")
    response = fields.Str()
    date_created = fields.DateTime()
    date_modified = fields.DateTime()

    @post_load
    def make_response(self, data, **kwargs):
        return Response(**data)
