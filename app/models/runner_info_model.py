from app import db


# Information about a user who is a runner. All of this info is not tournament-specific.
class RunnerInfo(db.Model):
    __tablename__ = "runner_info"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    srl_name = db.Column(db.String(60), nullable=False)
    twitch_name = db.Column(db.String(60), nullable=False)
    src_name = db.Column(db.String(60), nullable=False)
    availability_weekday = db.Column(db.String(120))
    availability_weekend = db.Column(db.String(120))
    input_method = db.Column(db.String(60), nullable=False)
    timezone = db.Column(db.String(10))

    user = db.relationship("User", back_populates="runner_info", uselist=False, lazy="joined")

    def __repr__(self):
        return "<RunnerInfo %s>" % self.user.username
