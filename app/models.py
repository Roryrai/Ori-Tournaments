from app import db
from app import login
from datetime import datetime
from sqlalchemy_utils import LtreeType
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

import random
import string


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Top-level tournament object. Most things are accessible from somewhere in here
class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    category = db.Column(db.String(60), nullable=False)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    signups_open = db.Column(db.DateTime())
    signups_close = db.Column(db.DateTime())
    visible = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(60))
    active = db.Column(db.Boolean, default=False)

    questions = db.relationship("Question", back_populates="tournament", lazy="dynamic")
    bracket_nodes = db.relationship("BracketNode", back_populates="tournament", lazy="dynamic")
    races = db.relationship("Race", back_populates="tournament", lazy="dynamic")
    groups = db.relationship("RunnerGroup", back_populates="tournament", lazy="dynamic")
    seeds = db.relationship("RunnerSeed", back_populates="tournament", lazy="dynamic")
    entrants = db.relationship("Entrant", back_populates="tournament", lazy="dynamic")

    def registration_open(self):
        if self.signups_open is not None and self.signups_close is not None:
            return self.signups_open <= datetime.utcnow() <= self.signups_close
        else:
            return False

    def __repr__(self):
        return "<Tournament %s>" % self.name


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
    tournaments = db.relationship("Entrant", back_populates="user", lazy="dynamic")

    # Password stuff
    def generate_salt(self):
        if self.salt is None:
            salt = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(32)])
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


# Tournament specific questions
class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
    question = db.Column(db.String(120), nullable=False)

    responses = db.relationship("Response", back_populates="question", lazy="dynamic")
    tournament = db.relationship("Tournament", back_populates="questions", uselist=False)
    def __repr__(self):
        return "<Question %s>" % self.question

# Association object for a user's responses to questions
class Response(db.Model):
    __tablename__ = "question_responses"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    response = db.Column(db.String(120), nullable=False)

    question = db.relationship("Question", back_populates="responses")
    user = db.relationship("User", back_populates="question_responses")

    def __repr__(self):
        return "<Response %s: %s - %s>" % (self.user, self.question, self.response)


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


# Races
class Race(db.Model):
    __tablename__ = "races"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    number_entrants = db.Column(db.Integer, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
    bracket_id = db.Column(db.Integer, db.ForeignKey("bracket.id"))
    comments = db.Column(db.String(500))

    tournament = db.relationship("Tournament", back_populates="races", uselist=False)
    bracket_node = db.relationship("BracketNode", back_populates="races", uselist=False)
    results = db.relationship("RaceResult", back_populates="race", lazy="dynamic")

    def __repr__(self):
        return "<Race %s - entrants: %s, bracket: %s>" % (self.date, self.number_entrants, self.bracket_node)


# Association table between races and users who participated in those races
class RaceResult(db.Model):
    __tablename__ = "race_participants"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    race_id = db.Column(db.Integer, db.ForeignKey("races.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    time = db.Column(db.Interval)
    comments = db.Column(db.String(120))

    race = db.relationship("Race", back_populates="results")
    user = db.relationship("User", back_populates="race_results")

    def __repr__(self):
        return "<RaceResult %s: %s>" % (self.user, self.time)


# Group names for group stage tournaments.
class GroupName(db.Model):
    __tablename__ = "group_names"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    group_name = db.Column(db.String(60), nullable=False)

    runner_groups = db.relationship("RunnerGroup", back_populates="group", lazy="dynamic")

    def __repr__(self):
        return "<GroupName %s>" % self.group_name


# Association table for putting runners into groups
class RunnerGroup(db.Model):
    __tablename__ = "runner_groups"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group_names.id"), nullable=False)

    tournament = db.relationship("Tournament", back_populates="groups")
    user = db.relationship("User", back_populates="groups")
    group = db.relationship("GroupName", back_populates="runner_groups")

    def __repr__(self):
        return "<RunnerGroup %s - %s>" % (self.user.username, self.group.group_name)


# Association table for giving runners a seed
class RunnerSeed(db.Model):
    __tablename__ = "runner_seeds"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    seed = db.Column(db.Integer, nullable=False)

    tournament = db.relationship("Tournament", back_populates="seeds")
    user = db.relationship("User", back_populates="seeds")


# Association table for putting runners into tournaments
class Entrant(db.Model):
    __tablename__ = "tournament_entrants"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)

    user = db.relationship("User", back_populates="tournaments")
    tournament = db.relationship("Tournament", back_populates="entrants")
