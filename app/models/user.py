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
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(60), nullable=False)
    discord_name = db.Column(db.String(60), nullable=False)
    pronunciation = db.Column(db.String(60))
    pronouns = db.Column(db.String(10), nullable=False)
    about = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    password_hash = db.Column(db.String(128))
    salt = db.Column(db.String(32))
    organizer = db.Column(db.Boolean, default=False)

    runner_info = db.relationship("RunnerInfo", back_populates="user", uselist=False, lazy="joined")
    volunteer_info = db.relationship("VolunteerInfo", back_populates="user", uselist=False, lazy="joined")
    question_responses = db.relationship("Response", back_populates="user", lazy="dynamic")
    bracket_nodes = db.relationship("BracketNode", back_populates="user", lazy="dynamic")
    race_results = db.relationship("RaceResult", back_populates="user", lazy="dynamic")
    groups = db.relationship("RunnerGroup", back_populates="user", lazy="dynamic")
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
        if self.is_registered(tournament_id):
            registration = Entrant.query.filter_by(user_id=self.id, tournament_id=tournament_id).first()
            db.session.delete(registration)
            db.session.commit()

    def is_registered(self, tournament_id):
        return Entrant.query.filter_by(user_id=self.id, tournament_id=tournament_id).first() is not None

    # Functions to extract stuff from other fields
    def is_runner(self):
        return self.runner_info is not None

    def is_volunteer(self):
        return self.volunteer_info is not None

    def is_restream(self):
        return self.is_volunteer() and self.volunteer_info.restream

    def is_commentary(self):
        return self.is_volunteer() and self.volunteer_info.commentary

    def is_tracking(self):
        return self.is_volunteer() and self.volunteer_info.tracking

    def is_organizer(self):
        return self.organizer

    def __repr__(self):
        return "<User %s>" % self.username
