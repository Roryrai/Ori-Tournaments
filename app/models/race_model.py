from app import db
from datetime import datetime


# Races
class Race(db.Model):
    __tablename__ = "race"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    number_entrants = db.Column(db.Integer, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id"), nullable=False)
    bracket_id = db.Column(db.Integer, db.ForeignKey("bracket_node.id"))
    comments = db.Column(db.String(500))

    tournament = db.relationship("Tournament", back_populates="races", uselist=False)
    bracket_node = db.relationship("BracketNode", back_populates="races", uselist=False)
    results = db.relationship("RaceResult", back_populates="race", lazy="dynamic")

    def __repr__(self):
        return "<Race %s - entrants: %s, bracket: %s>" % (self.date, self.number_entrants, self.bracket_node)
