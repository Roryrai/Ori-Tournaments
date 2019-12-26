from app import db
from datetime import datetime


# Association table between races and users who participated in those races
# Each record holds a single runner's time and a reference to the race it happened in
class RaceResult(db.Model):
    __tablename__ = "race_result"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    race_id = db.Column(db.Integer, db.ForeignKey("race.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    time = db.Column(db.Interval)
    comments = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)

    race = db.relationship("Race", back_populates="results")
    user = db.relationship("User", back_populates="race_results")

    def __repr__(self):
        return "<RaceResult %s: %s>" % (self.user, self.time)
