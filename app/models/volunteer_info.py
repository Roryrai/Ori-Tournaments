from app import db


# Information about a user who is a volunteer. All of this is not tournament-specific.
class VolunteerInfo(db.Model):
    __tablename__ = "volunteer_info"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    restream = db.Column(db.Boolean, nullable=False)
    commentary = db.Column(db.Boolean, nullable=False)
    tracking = db.Column(db.Boolean, nullable=False)
    organizer = db.Column(db.Boolean, nullable=False)

    user = db.relationship("User", back_populates="volunteer_info", uselist=False, lazy="joined")

    def __repr__(self):
        return "<VolunteerInfo %s>" % self.user.username
