from app import db
from sqlalchemy_utils import LtreeType


# Each BracketNode represents a single point in the bracket.
# Two BracketNodes are a match
# best_of = runners play a best of X to reach this node
class BracketNode(db.Model):
    __tablename__ = "bracket"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    node = db.Column(db.String(10), nullable=False)
    path = db.Column(LtreeType, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
    best_of = db.Column(db.Integer)

    races = db.relationship("Race", back_populates="bracket_node")
    tournament = db.relationship("Tournament", back_populates="bracket_nodes", uselist=False)
    user = db.relationship("User", back_populates="bracket_nodes", uselist=False)

    def __repr__(self):
        return "<BracketNode %s - path: %s, runner: %s>" % (self.node, self.path, self.user)

