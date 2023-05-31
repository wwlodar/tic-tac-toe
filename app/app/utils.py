from flask import redirect


def redirect_if_not_logged_in(current_user):
    if not current_user.is_active:
        return redirect("/")
