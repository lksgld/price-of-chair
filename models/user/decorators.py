import functools
from typing import Callable
from flask import session, flash, redirect, url_for, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)      # the original function keeps its name and description
    def decorated_function(*args, **kwargs):     # function can have any number of arguments and key arguments
        if not session.get("email"):
            flash("You need to be logged in.", "danger")
            return redirect(url_for("users.login_user"))
        return f(*args, **kwargs)
    return decorated_function   # returning the function! not the output


def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") != current_app.config.get("ADMIN", ""):
            flash("You need to be an admin to access this page.", "danger")
            return redirect(url_for("users.login_user"))
        return f(*args, **kwargs)

    return decorated_function
