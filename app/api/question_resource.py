from datetime import datetime
from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app import db
from app.models import Question
from app.schemas import QuestionSchema
from app.security import Security
from app.security import role_organizer

class QuestionResource(Resource):
    schema = QuestionSchema()
    list_schema = QuestionSchema(many=True)

    @jwt_required
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

    @role_organizer
    def post(self):
        data = request.get_json()
        question = self.schema.load(data)
        try:
            db.session.add(question)
            db.session.commit()
        except:
            db.session.rollback()
        return self.schema.dump(question), 201

    @role_organizer
    def put(self):
        data = request.get_json()
        new_question = self.schema.load(data)
        question = Question.query.get(new_question.id)
        if question:
            question.question = new_question.question
            question.tournament_id = new_question.tournament_id
            question.date_modified = datetime.utcnow()
            db.session.commit()
            return
        else:
            abort(404)

    @role_organizer
    def delete(self):
        question = Question.query.get(request.args.get("id"))
        if question:
            db.session.delete(question)
            db.session.commit()
            return
        else:
            abort(404)
