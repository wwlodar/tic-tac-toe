from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from app.app import forms
from app.app.models import User
from app.app.stats import get_user_stats
from app.extensions import db
from app.run import app


@app.route("/", methods=["GET", "POST"])
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


@app.route("/home")
def homepage():
    if current_user.is_active == False:
        return redirect(url_for("assign_username"))
    else:
        return render_template("home.html", current_user=current_user)


@app.route("/health")
def health():
    return {"message": "It works!"}


@app.route("/game")
def game():
    if current_user.is_active == False:
        return redirect(url_for("assign_username"))

    return render_template("game.html", current_user=current_user)


@app.route("/stats")
def stats():
    if current_user.is_active == False:
        return redirect(url_for("assign_username"))
    else:
        stats = get_user_stats(current_user)
        return render_template("stats.html", current_user=current_user, stats=stats)


@app.route("/add_points")
def add_points():
    redirect_if_not_logged_in(current_user)
    if current_user.added_points == False:
        current_user.points += 10
        current_user.added_points = True
        db.session.commit()

        flash("You added 10 points!")
        return render_template("home.html", current_user=current_user)
    else:
        flash("You already added 10 points, you cannot do it again")
        return render_template("home.html", current_user=current_user)
