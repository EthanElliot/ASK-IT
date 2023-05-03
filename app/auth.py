from crypt import methods
from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import SignUpForm,SignInForm
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


auth = Blueprint("auth", __name__)


@auth.route("/signin", methods=['GET','POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter((User.email == str(form.identifier.data)) |(User.username == str(form.identifier.data))).first() 
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("home.default"))
            else:
                flash("invalid username or passowrd")   
                return render_template("signin.html", form=form)
                    
        else: 
            flash("invalid username or passowrd")   
            return render_template("signin.html", form=form)

    return render_template("signin.html", form=form)


@auth.route("/signup", methods=['GET','POST'])
def signup():
    form = SignUpForm() 
    if form.validate_on_submit():
        print(form.username)
        user=User.query.first()
        new_user = User(username=(form.username.data),email=(form.email.data),password=generate_password_hash(form.password.data), verified=True)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("home.default"))



    return render_template("signup.html",form=form)



@auth.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.signin'))





    