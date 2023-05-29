from flask import Blueprint, render_template,redirect,url_for,flash
from extentions import db, SignInForm ,SignUpForm
from models import User
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user,logout_user

api = Blueprint('', __name__)


@api.get('/')
def home():
    return render_template("home.html")


@api.route('/u/<int:id>')
def user(id):
    user = User.query.filter(User.id==id).first_or_404()
    return render_template("user.html", user=user)


@api.route('/signin',methods=['GET','POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter((User.email == str(form.identifier.data)) |(User.username == str(form.identifier.data))).first() 
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("invalid username or passowrd")   
                return render_template("signin.html", form=form)
        else: 
            flash("invalid username or passowrd")   
            return render_template("signin.html", form=form)
    return render_template("signin.html", form=form)


@api.route("/signup", methods=['GET','POST'])
def signup():
    form = SignUpForm() 
    if form.validate_on_submit():
        new_user = User(username=(form.username.data),email=(form.email.data),password=generate_password_hash(form.password.data), verified=True)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("signup.html",form=form)


@api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
