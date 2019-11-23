from app import db


# Tournament specific questions
class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
    question = db.Column(db.String(120), nullable=False)

    responses = db.relationship("Response", back_populates="question", lazy="dynamic")
    tournament = db.relationship("Tournament", back_populates="questions", uselist=False)

    def __repr__(self):
        return "<Question %s>" % self.question
