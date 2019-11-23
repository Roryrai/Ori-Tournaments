from app import db


# Association table between races and users who participated in those races
class RaceResult(db.Model):
    __tablename__ = "race_participants"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    race_id = db.Column(db.Integer, db.ForeignKey("races.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    time = db.Column(db.Interval)
    comments = db.Column(db.String(120))

    race = db.relationship("Race", back_populates="results")
    user = db.relationship("User", back_populates="race_results")

    def __repr__(self):
        return "<RaceResult %s: %s>" % (self.user, self.time)
