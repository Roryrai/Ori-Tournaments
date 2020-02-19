from datetime import datetime
from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_optional

from app import db
from app.models import Question
from app.schemas import QuestionSchema
from app.security import Security
from app.security import role_organizer

class QuestionResource(Resource):
    schema = QuestionSchema()
    list_schema = QuestionSchema(many=True)

    @jwt_optional
    def get(self):
        args = request.args
        if "id" in args and len(args) is not 1:
            return "'id' parameter may not be used with other parameters", 400

        question_id = args.get("id")

        tournament_id = args.get("tournament_id")
        text = args.get("text")
        sort = args.get("sort")
        reverse = args.get("reverse") == "true"

        query = Question.query

        # Get one by id
        if question_id:
            query = query.filter(Question.id == question_id)

        # Build query
        if tournament_id:
            query = query.filter(Question.tournament_id == tournament_id)
        if text:
            text = "%" + text + "%"
            query = query.filter(Question.question.ilike(text))

        order = Question.id
        if sort == "question":
            order = Question.question
        if reverse:
            order = order.desc()
        query = query.order_by(order)
        questions = query.all()

        return self.list_schema.dump(questions)