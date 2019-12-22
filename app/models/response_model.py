from app import db


# Association object for a user's responses to questions
class Response(db.Model):
    __tablename__ = "question_response"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    response = db.Column(db.String(120), nullable=False)

    question = db.relationship("Question", back_populates="responses")
    user = db.relationship("User", back_populates="question_responses")

    def __repr__(self):
        return "<Response %s: %s - %s>" % (self.user, self.question, self.response)
