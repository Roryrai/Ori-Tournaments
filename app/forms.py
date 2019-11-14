from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import RadioField
from wtforms import SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from app.models import User
from datetime import date

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


# Form for creating an account
class CreateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    discord_name = StringField("Discord Name", validators=[DataRequired()])
    pronunciation = StringField("How is your username pronounced?", validators=[DataRequired()])
    pronouns = RadioField("What are your preferred pronouns?", choices=[("he/him", "He/Him"), ("she/her", "She/Her"), ("they/them", "They/Them")], validators=[DataRequired()])
    interesting_facts = StringField("What are some interesting facts about yourself?")
    submit = SubmitField("Create Account")

    def validate_username(form, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("That username is taken")


# Form for users who don't have a profile in the database already
class NewRegistrationForm(FlaskForm):
    runner = RadioField(choices=[("yes", "Yes"), ("no", "No")], validators=[DataRequired()])
    runner.label = "Will you be participating as a runner?"
    srl_name = StringField("SpeedRunsLive Name", validators=[DataRequired()])
    twitch_name = StringField("Twitch Name", validators=[DataRequired()])
    src_name = StringField("Speedrun.com Name", validators=[DataRequired()])
    input_method = RadioField("Input Method", choices=[("kbm", "Keyboard & Mouse"), ("controller", "Controller"), ("hybrid", "Hybrid"), ("other", "Other")], validators=[DataRequired()])
    other_input_method = StringField("Other Input Method (Please specify)")

    volunteer = RadioField("Will you be participating as a volunteer?", choices=[("yes", "Yes"), ("no", "No")], validators=[DataRequired()])
    restream = BooleanField("Are you able and willing to restream tournament matches?")
    commentary = BooleanField("Are you interested in providing commentary for tournament matches?")
    tracking = BooleanField("Are you interested in tracking stats and providing information to commentators during races?")
    submit = SubmitField("Submit Registration")

    def validate_other_input_method(form, other_input_method):
        if form.input_method.data == "Other" and (other_input_method.data is None or other_input_method.data == ""):
            raise ValidationError("Please specify your input method")


# Form for runners who already have their profiles filled out
class ExistingRegistrationForm(FlaskForm):
    submit = SubmitField("Register")

class CreateTournamentForm(FlaskForm):
    name = StringField("Tournament Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    signups_open = DateField("Signups Open", validators=[DataRequired()])
    signups_close = DateField("Signups Close", validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("Anticipated End Date", validators=[DataRequired()])
    visible = BooleanField("Visible")
    submit = SubmitField("Create Tournament", validators=[DataRequired()])

    def validate_signups_open(form, signups_open):
        if signups_open.data < date.today():
            raise ValidationError("Signups should open in the future.")

    def validate_signups_close(form, signups_close):
        if signups_close.data < form.signups_open.data:
            raise ValidationError("Signups must be open before they close.")

    def validate_start_date(form, start_date):
        if start_date.data < date.today():
            raise ValidationError("Start date must be in the future.")
        if start_date.data < form.signups_open.data:
            raise ValidationError("Start date must be after signups open.")

    def validate_end_date(form, end_date):
        if end_date.data < form.start_date.data:
            raise ValidationError("End date must be after start date.")
