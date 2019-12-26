from sqlalchemy import UniqueConstraint
from datetime import datetime
from app import db


# Association table for putting runners into groups
class GroupMember(db.Model):
    __tablename__ = "group_member"
    __table_args__ = (UniqueConstraint("user_id",
                                       "tournament_id",
                                       name="unique_tournament_group_constraint"),)

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group_name.id"), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    tournament = db.relationship("Tournament", back_populates="groups")
    user = db.relationship("User", back_populates="groups")
    group = db.relationship("GroupName", back_populates="runner_groups")

    def __repr__(self):
        return "<RunnerGroup %s - %s>" % (self.user.username, self.group.group_name)
