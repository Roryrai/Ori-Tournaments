from datetime import datetime
from flask import request
from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app import db
from app.models import Question
from app.models import Response
from app.schemas import ResponseSchema
from app.security import Security
from app.security import role_organizer

class ResponseResource(Resource):
    schema = ResponseSchema()
    list_schema = ResponseSchema(many=True)

    def get(self):
        args = request.args
        if "id" in args and len(args) is not 1:
            return "'id' parameter may not be used with other parameters", 400

        response_id = args.get("id")
        question_id = args.get("question_id")
        tournament_id = args.get("tournament_id")
        user_id = args.get("user_id")
        sort = args.get("sort")
        reverse = args.get("reverse") == "true"

        query = Response.query

        if response_id:
            query = query.filter(Response.id == response_id)

        if question_id:
            query = query.filter(Response.question_id == question_id)
        if tournament_id:
            query = query.filter(Response.question.has(Question.tournament_id == tournament_id))
        if user_id:
            query = query.filter(Response.user_id == user_id)

        # Default sort by question
        order = Response.question_id
        if sort == "tournament_id":
            order = Response.question.tournament_id
        if reverse:
            order = order.desc()
        query = query.order_by(order)
        responses = query.all()

        return self.list_schema.dump(responses)

    @jwt_required
    def post(self):
        data = request.get_json()
        user_id = Security.get_current_user().id
        data["user_id"] = user_id

        response = self.schema.load(data)
        db.session.add(response)
        db.session.commit()
        return None, 201

    @jwt_required
    def put(self):
        data = request.get_json()
        new = self.schema.load(data)
        user_id = Security.get_current_user().id
        # Get existing response only if it belongs to the current user
        response = Response.query.get(new.id)

        if response:
            print(response.user_id, user_id)
            if response.user_id is not user_id:
                return "You are not authorized to edit this response.", 401
            response.response = new.response
            response.modified_date = datetime.utcnow()
            db.session.commit()
            return
        else:
            return None, 404

    @role_organizer
    def delete(self):
        id = request.args.get("id")
        response = Response.query.get(id)
        if response:
            db.session.delete(response)
            db.session.commit()
        else:
            return None, 404







