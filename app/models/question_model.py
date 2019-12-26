from app import db
from datetime import datetime

# Tournament specific questions
class Question(db.Model):
    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id"), nullable=False)
    question = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    
    responses = db.relationship("Response", back_populates="question", lazy="dynamic")
    tournament = db.relationship("Tournament", back_populates="questions", uselist=False)

    def __repr__(self):
        return "<Question %s>" % self.question
