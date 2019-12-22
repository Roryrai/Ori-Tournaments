from app import db


class Volunteer(db.Model):
    __tablename__ = "tournament_volunteer"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id"), nullable=False)

    user = db.relationship("User", back_populates="tournaments_volunteered")
    tournament = db.relationship("Tournament", back_populates="volunteers")
