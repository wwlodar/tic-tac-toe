from enum import Enum

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.app import forms
from app.app.models import Game, User, UserGames
from app.extensions import db

bp = Blueprint("myapp", __name__)


@bp.route("/", methods=["GET", "POST"])
def assign_username():
    if not current_user.is_active:
        form = forms.NameForm()
        print(form.username)
        if request.method == "POST":
            if form.validate_on_submit():
                new_user = User(username=form.username.data)
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user)
                return redirect("/home")
            else:
                flash("Username must have between 1 and 30 characters")

        return render_template("username.html", form=form)

    else:
        return redirect("/home")


@bp.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("myapp.assign_username"))


@bp.route("/home")
def homepage():
    if current_user.is_active == False:
        return redirect(url_for("myapp.assign_username"))
    else:
        return render_template("home.html", current_user=current_user)


@bp.route("/health")
def health():
    return {"message": "It works!"}


@bp.route("/game")
def game():
    if current_user.is_active == False:
        return redirect(url_for("myapp.assign_username"))

    return render_template("game.html", current_user=current_user)


@bp.app_template_filter("enum_to_val")
def enum_to_val(obj):
    if isinstance(obj, Enum):
        return obj.value

    return obj


@bp.route("/stats")
def statistics():
    if current_user.is_active == False:
        return redirect(url_for("myapp.assign_username"))
    else:
        stats = UserGames.query.filter_by(user_id=current_user.id).join(Game).all()
        return render_template("stats.html", current_user=current_user, stats=stats)


@bp.route("/add_points")
def add_points():
    if current_user.is_active == False:
        return redirect(url_for("myapp.assign_username"))
    if current_user.added_points == False:
        current_user.points += 10
        current_user.added_points = True
        db.session.commit()

        flash("You added 10 points!")
        return render_template("home.html", current_user=current_user)
    else:
        flash("You already added 10 points, you cannot do it again")
        return render_template("home.html", current_user=current_user)
