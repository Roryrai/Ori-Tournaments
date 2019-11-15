from app import app
from app import db
from app.models import User
from app.models import Tournament
from app.models import RunnerInfo
from app.models import VolunteerInfo
from app.forms import LoginForm
from app.forms import ExistingRegistrationForm
from app.forms import CombinedRegistrationForm
from app.forms import CreateAccountForm
from app.forms import CreateTournamentForm
from app.forms import EditProfileForm

from datetime import datetime

from flask import render_template
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask import abort

from werkzeug.urls import url_parse

from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required



@app.route("/")
@app.route("/index")
def index():
    now = datetime.utcnow()
    tournaments = Tournament.query.filter(Tournament.signups_open <= now, now <= Tournament.end_date, Tournament.visible != False).all()
    return render_template("index.html", user=current_user, tournaments=tournaments)


@app.route("/newuser", methods=["GET", "POST"])
def newuser():
    if current_user.is_authenticated:
        return redirec(url_for("index"))
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.set_password(form.password.data)
        user.discord_name = form.discord_name.data
        user.pronunciation = form.pronunciation.data
        user.pronouns = form.pronouns.data
        user.interesting_facts = form.interesting_facts.data
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
        return redirect(url_for("index"))
    return render_template("create_account.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/user/<username>")
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # Update user
        flash("Profile updated (except not really)")
        return redirect(url_for("user", username=current_user.username))
    elif request.method == "GET":
        # Populate form
        form.discord_name.data = current_user.discord_name
        form.pronunciation.data = current_user.pronunciation
        form.pronouns.data = current_user.pronouns
        form.interesting_facts.data = current_user.interesting_facts

        if current_user.runner_info is not None:
            form.runner_info_required()
            form.twitch_name.data = current_user.runner_info.twitch_name
            form.srl_name.data = current_user.runner_info.srl_name
            form.src_name.data = current_user.runner_info.src_name
            form.input_method.data = current_user.runner_info.input_method

        if current_user.volunteer_info is not None:
            form.restream.data = "yes" if current_user.volunteer_info.restream else "no"
            form.commentary.data = "yes" if current_user.volunteer_info.commentary else "no"
            form.tracking.data = "yes" if current_user.volunteer_info.tracking else "no"
    return render_template("edit_profile.html", title="Edit Profile", form=form)

@app.route("/tournaments")
def tournaments():
    now = datetime.utcnow()
    # Active tournaments - signups have opened and the tournament has not concluded
    active = Tournament.query.filter_by(active=True, visible=True)
    # Inactive tournaments - signups are not yet open or the tournament has concluded
    inactive = Tournament.query.filter_by(active=False, visible=True)
    # Planned tournaments - flagged as visible=false by organizers - active status doesn't matter
    planned = Tournament.query.filter_by(visible=False)
    return render_template("tournaments.html", title="Tournament List", tournaments=active, history=inactive, planned = planned)

@app.route("/tournaments/new", methods=["GET", "POST"])
@login_required
def create_tournament():
    if not current_user.is_organizer():
        return abort(404)
    form = CreateTournamentForm()
    if form.validate_on_submit():
        tournament = Tournament()
        tournament.name = form.name.data
        tournament.category = form.category.data
        tournament.signups_open = form.signups_open.data
        tournament.signups_close = form.signups_close.data
        tournament.start_date = form.start_date.data
        tournament.end_date = form.end_date.data
        tournament.visible = form.visible.data
        db.session.add(tournament)
        db.session.commit()
        flash("%s has been created." % tournament.name)
        return redirect(url_for("tournaments"))
    return render_template("create_tournament.html", title="Create Tournament", form=form)


@app.route("/tournaments/<tournament_id>")
def tournament_details(tournament_id):
    tournament = Tournament.query.get(tournament_id)
    if tournament is None:
        return redirect(url_for("tournaments"))
    return render_template("tournament_details.html", title="%s" % tournament.name, tournament=tournament)

@app.route("/tournaments/<tournament_id>/register", methods=["GET", "POST"])
@login_required
def register(tournament_id):
    tournament = Tournament.query.get(tournament_id)
    if current_user.runner_info is not None:
        form = ExistingRegistrationForm()
        if form.validate_on_submit():
            current_user.register(tournament_id)
            flash("Your registration has been received. We ask that you verify that all information on your profile is correct prior to the start of the event.")
            return redirect(url_for("index"))
    else:
        form = CombinedRegistrationForm()
        if form.validate_on_submit():
            runner_info = RunnerInfo()
            runner_info.srl_name = form.srl_name.data
            runner_info.twitch_name = form.twitch_name.data
            runner_info.src_name = form.src_name.data
            runner_info.input_method = form.input_method.data if form.input_method.data is not None else form.other_input_method.data
            runner_info.availability_weekday = "All"
            runner_info.availability_weekend = "All"


            volunteer_info = VolunteerInfo()
            volunteer_info.restream = form.restream.data
            volunteer_info.commentary = form.commentary.data
            volunteer_info.tracking = form.tracking.data
            volunteer_info.organizer = False

            current_user.runner_info = runner_info
            current_user.volunteer_info = volunteer_info

            current_user.register(tournament_id)
            db.session.commit()

            flash("Your registration has been received.")
            return redirect(url_for("index"))
    return render_template("register.html", title="Register - %s" % tournament.name, form=form, tournament=tournament)

@app.route("/tournaments/<tournament_id>withdraw")
@login_required
def withdraw_registration(tournament_id):
    current_user.withdraw(tournament_id)
    flash("Your registration has been withdrawn.")
    return redirect(url_for("index"))

@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html")
