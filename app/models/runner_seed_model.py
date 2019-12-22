from app import db


# Association table for giving runners a seed
class RunnerSeed(db.Model):
    __tablename__ = "runner_seed"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    seed = db.Column(db.Integer, nullable=False)

    tournament = db.relationship("Tournament", back_populates="seeds")
    user = db.relationship("User", back_populates="seeds")
