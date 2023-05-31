from flask import flash, redirect, render_template
from flask_login import current_user, login_user

from app.app import forms
from app.app.models import User
from app.app.utils import redirect_if_not_logged_in
from app.extensions import db
from app.run import app


@app.route("/", methods=["GET", "POST"])
def assign_username():
    if not current_user.is_active:
        form = forms.NameForm()
        print(form.username)
        if form.validate_on_submit():
            new_user = User(username=form.username.data)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect("/home")
        else:
            flash("Incorrect username!")

        return render_template("username.html", form=form)

    else:
        return redirect("/home")


@app.route("/home")
def homepage():
    redirect_if_not_logged_in(current_user)
    return render_template("home.html", current_user=current_user)


@app.route("/health")
def health():
    return {"message": "It works!"}


@app.route("/game")
def game():
    redirect_if_not_logged_in(current_user)
    # get player 1  -> wait until player 2 connects
    # if more players -> wait for user with status waiting
    # after that change player status to in game and randomize who gets O and X
    # start the timer and the game

    # once game finishes -> wait 1 sec; redirect to homepage, show message ("Won/lost/tied")
    return {"Message": "Game is on"}


@app.route("/stats")
def stats():
    redirect_if_not_logged_in(current_user)
    # if username
    # else redirect to assign_username
    return {"Message": "Your stats"}


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
