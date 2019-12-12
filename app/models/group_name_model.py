from app import db


# Group names for group stage tournaments.
class GroupName(db.Model):
    __tablename__ = "group_names"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    group_name = db.Column(db.String(60), nullable=False)

    runner_groups = db.relationship("GroupMember", back_populates="group", lazy="dynamic")

    def __repr__(self):
        return "<GroupName %s>" % self.group_name
