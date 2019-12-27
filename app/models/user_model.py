from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

from app.models import Entrant

import random
import string


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User object
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(60), nullable=False, unique=True)
    discord_name = db.Column(db.String(60), nullable=False)
    pronunciation = db.Column(db.String(60))
    pronouns = db.Column(db.String(10), nullable=False)
    about = db.Column(db.String(500))
    date_created = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    date_modified = db.Column(db.DateTime(), default = datetime.utcnow, nullable=False)
    password_hash = db.Column(db.String(128))
    salt = db.Column(db.String(32))
    organizer = db.Column(db.Boolean, default=False)
    twitch_name = db.Column(db.String(128))
    srl_name = db.Column(db.String(128))
    src_name = db.Column(db.String(128))
    input_method = db.Column(db.String(60))
    availability_weekday = db.Column(db.String(256))
    availability_weekend = db.Column(db.String(256))
    timezone = db.Column(db.String(60))
    restream = db.Column(db.Boolean, default=False)
    commentary = db.Column(db.Boolean, default=False)
    tracking = db.Column(db.Boolean, default=False)


    question_responses = db.relationship("Response", back_populates="user", lazy="dynamic")
    bracket_nodes = db.relationship("BracketNode", back_populates="user", lazy="dynamic")
    race_results = db.relationship("RaceResult", back_populates="user", lazy="dynamic")
    groups = db.relationship("GroupMember", back_populates="user", lazy="dynamic")
    seeds = db.relationship("RunnerSeed", back_populates="user", lazy="dynamic")
    tournaments_entered = db.relationship("Entrant", back_populates="user", lazy="dynamic")
    tournaments_volunteered = db.relationship("Volunteer", back_populates="user", lazy="dynamic")

    # Password stuff
    def generate_salt(self):
        if self.salt is None:
            salt = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation)
                            for n in range(32)])
            self.salt = salt

    def set_password(self, password):
        if self.salt is None:
            self.generate_salt()
        self.password_hash = generate_password_hash(password + self.salt)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + self.salt)

    # Registration for the specified tournament
    def register(self, tournament_id):
        if not self.is_registered(tournament_id):
            entrant = Entrant(user_id=self.id, tournament_id=tournament_id)
            db.session.add(entrant)
            db.session.commit()

    def withdraw(self, tournament_id):
        registration = Entrant.query.filter_by(user_id=self.id, tournament_id=tournament_id).first()
        if registration is not None:
            db.session.delete(registration)
            db.session.commit()

    def is_registered(self, tournament_id):
        return Entrant.query.filter_by(user_id=self.id, tournament_id=tournament_id).first() is not None

    # Functions to extract stuff from other fields
    def is_runner(self):
        return self.twitch_name is not None

    def is_volunteer(self):
        return self.commentary and self.restream and self.tracking

    def is_restream(self):
        return self.restream

    def is_commentary(self):
        return self.commentary

    def is_tracking(self):
        return self.tracking

    def is_organizer(self):
        return self.organizer

    def __repr__(self):
        return "<User %s>" % self.username
