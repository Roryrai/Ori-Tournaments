from sqlalchemy import UniqueConstraint
from app import db
from datetime import datetime


class Volunteer(db.Model):
    __tablename__ = "tournament_volunteer"
    __table_args__ = (UniqueConstraint("user_id",
                                       "tournament_id",
                                       name="unique_tournament_volunteer_constraint"),)

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id"), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    user = db.relationship("User", back_populates="tournaments_volunteered")
    tournament = db.relationship("Tournament", back_populates="volunteers")
