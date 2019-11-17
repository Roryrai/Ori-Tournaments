from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import RadioField
from wtforms import SubmitField
from wtforms.fields import TextAreaField
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
    interesting_facts = TextAreaField("What are some interesting facts about yourself?")
    submit = SubmitField("Create Account")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("That username is taken.")


class EditProfileForm(FlaskForm):
    # General info
    current_password = PasswordField("Current Password")
    new_password = PasswordField("Update Password")
    new_password2 = PasswordField("Confirm Password", validators=[EqualTo("new_password")])
    discord_name = StringField("Discord Name", validators=[DataRequired()])
    pronunciation = StringField("How is your username pronounced?", validators=[DataRequired()])
    pronouns = RadioField("What are your preferred pronouns?", choices=[("he/him", "He/Him"), ("she/her", "She/Her"), ("they/them", "They/Them")], validators=[DataRequired()])
    interesting_facts = TextAreaField("What are some interesting facts about yourself?")

    # Runner info
    srl_name = StringField("SpeedRunsLive Name")
    twitch_name = StringField("Twitch Name")
    src_name = StringField("Speedrun.com Name")
    input_method = RadioField("Input Method", choices=[("na", "N/A - Not a runner"), ("kbm", "Keyboard & Mouse"), ("controller", "Controller"), ("hybrid", "Hybrid"), ("other", "Other")], default="na")
    other_input_method = StringField("Other input method (Please specify)")

    # Volunteer info
    restream = RadioField("Are you able and willing to restream tournament matches?", choices=[("yes", "Yes"), ("no", "No")], default="no")
    commentary = RadioField("Are you interested in providing commentary for tournament matches?", choices=[("yes", "Yes"), ("no", "No")], default="no")
    tracking = RadioField("Are you interested in tracking stats and providing information to commentators during races?", choices=[("yes", "Yes"), ("no", "No")], default="no")
    submit = SubmitField("Save")

    validate_runner_info = False

    def runner_info_required(self):
        self.srl_name.validators = [DataRequired()]
        self.twitch_name.validators = [DataRequired()]
        self.src_name.validators = [DataRequired()]
        self.input_method.validators = [DataRequired()]

    def has_runner_info(self):
        return (self.twitch_name.data is not None and self.twitch_name.data is not "") and \
                    (self.srl_name.data is not None and self.srl_name.data is not "") and \
                    (self.src_name.data is not None and self.src_name.data is not "") and \
                    (self.input_method.data is not "na")

    def validate_runner_tab(self):
        if (self.twitch_name.data is not None or self.twitch_name.data is not "") or \
                (self.srl_name.data is not None or self.srl_name.data is not "") or \
                (self.src_name.data is not None or self.src_name.data is not "") or \
                (self.input_method.data is not "na"):
            if (self.twitch_name.data is None or self.twitch_name.data is "") or \
                    (self.srl_name.data is None or self.srl_name.data is "") or \
                    (self.src_name.data is None or self.src_name.data is "") or \
                    (self.input_method.data is "na"):
                raise ValidationError("You must fill out all sections of runner info or none of them.")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("That username is taken.")

    def validate_other_input_method(self, other_input_method):
        if self.input_method.data == "Other" and (other_input_method.data is None or other_input_method.data == ""):
            raise ValidationError("Please specify your input method.")

    def validate_update_password(self, update_password):
        if update_password.data is not None and update_password.data is not "":
            if not current_user.check_password(self.current_password.data):
                raise ValidationError("Your current password is incorrect.")


# Form for users who don't have a profile in the database already
class CombinedRegistrationForm(FlaskForm):
    runner = RadioField("Will you be participating as a runner?", choices=[("yes", "Yes"), ("no", "No")], validators=[DataRequired()])
    srl_name = StringField("SpeedRunsLive Name", validators=[DataRequired()])
    twitch_name = StringField("Twitch Name", validators=[DataRequired()])
    src_name = StringField("Speedrun.com Name", validators=[DataRequired()])
    input_method = RadioField("Input Method", choices=[("kbm", "Keyboard & Mouse"),
                                                       ("controller", "Controller"),
                                                       ("hybrid", "Hybrid"),
                                                       ("other", "Other")], validators=[DataRequired()])
    other_input_method = StringField("Other Input Method (Please specify)")

    volunteer = RadioField("Will you be participating as a volunteer?", choices=[("yes", "Yes"), ("no", "No")],
                           validators=[DataRequired()])
    restream = BooleanField("Are you able and willing to restream tournament matches?")
    commentary = BooleanField("Are you interested in providing commentary for tournament matches?")
    tracking = BooleanField("Are you interested in tracking stats and providing information to \
                            commentators during races?")
    submit = SubmitField("Submit Registration")

    def validate_other_input_method(self, other_input_method):
        if self.input_method.data == "Other" and (other_input_method.data is None or other_input_method.data == ""):
            raise ValidationError("Please specify your input method.")


class RunnerRegistrationForm(FlaskForm):
    pass


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

    def validate_signups_open(self, signups_open):
        if signups_open.data < date.today():
            raise ValidationError("Signups should open in the future.")

    def validate_signups_close(self, signups_close):
        if signups_close.data < self.signups_open.data:
            raise ValidationError("Signups must be open before they close.")

    def validate_start_date(self, start_date):
        if start_date.data < date.today():
            raise ValidationError("Start date must be in the future.")
        if start_date.data < self.signups_open.data:
            raise ValidationError("Start date must be after signups open.")

    def validate_end_date(self, end_date):
        if end_date.data < self.start_date.data:
            raise ValidationError("End date must be after start date.")


class EditTournamentForm(FlaskForm):
    pass


class RaceResultForm(FlaskForm):
    pass


class EditRaceResultForm(FlaskForm):
    pass
