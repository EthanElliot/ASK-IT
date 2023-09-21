# imports
from flask import Blueprint, render_template, redirect, url_for,\
    flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from extentions import db
from forms import SignInForm, SignUpForm
from models import User


auth = Blueprint('auth', __name__)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    '''sigin route'''
    # if user is already logged in redirect
    if current_user.is_authenticated:
        return redirect(url_for("home.home_page"))
    # make and validate form
    form = SignInForm()
    if form.validate_on_submit():
        # check if user exits and log them in if the password matches
        user = User.query.filter((User.email == str(form.identifier.data)) | (
            User.username == str(form.identifier.data))).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("home.home_page"))
            else:
                flash("invalid username or passowrd")
                return render_template("signin.html", form=form)
        else:
            flash("invalid username or passowrd")
            return render_template("signin.html", form=form)
    return render_template("signin.html", form=form)


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    '''sigup route'''
    # if user is already logged in redirect
    if current_user.is_authenticated:
        return redirect(url_for("home.home_page"))
    # make and validate form
    form = SignUpForm()
    if form.validate_on_submit():
        # add user to db
        new_user = User(username=(form.username.data),
                        email=(form.email.data),
                        password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home.home_page"))
    return render_template("signup.html", form=form)


# logout route
@auth.route('/logout')
@login_required
def logout():
    '''logout route'''
    logout_user()
    return redirect(url_for("home.home_page"))
