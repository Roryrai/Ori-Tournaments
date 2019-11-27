from app import db
from datetime import datetime


# Top-level tournament object. Most things are accessible from somewhere in here
class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    category = db.Column(db.String(60), nullable=False)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    signups_open = db.Column(db.DateTime())
    signups_close = db.Column(db.DateTime())
    visible = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(60))
    active = db.Column(db.Boolean, default=False)

    questions = db.relationship("Question", back_populates="tournament", lazy="dynamic")
    bracket_nodes = db.relationship("BracketNode", back_populates="tournament", lazy="dynamic")
    races = db.relationship("Race", back_populates="tournament", lazy="dynamic")
    groups = db.relationship("Group", back_populates="tournament", lazy="dynamic")
    seeds = db.relationship("RunnerSeed", back_populates="tournament", lazy="dynamic")
    entrants = db.relationship("Entrant", back_populates="tournament", lazy="dynamic")
    volunteers = db.relationship("Volunteer", back_populates="tournament", lazy="dynamic")

    def registration_open(self):
        if self.signups_open is not None and self.signups_close is not None:
            return self.signups_open <= datetime.utcnow() <= self.signups_close
        else:
            return False

    def __repr__(self):
        return "<Tournament %s>" % self.name
