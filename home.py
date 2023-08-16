from datetime import datetime
from http.client import responses
from flask import Blueprint, render_template,redirect,url_for,flash,make_response,jsonify
from flask import request
from extentions import db
from forms import SignInForm ,SignUpForm,AskForm,ResponceForm
from models import User, Subject,Question,Response,Vote
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user,logout_user, current_user,login_required
import json


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


@api.route('/ask', methods=['GET','POST'])
@login_required
def ask():
    form = AskForm()
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]

    if form.validate_on_submit():
     
        body_md = (form.body.data[1:-1])
        new_post=Question(user_id=(current_user.id),subject_id=(form.subject.data), title=(form.title.data),date_posted=(datetime.now()),body=(body_md), views=0)
        db.session.add(new_post)
        db.session.commit()


        return redirect(url_for('question', id=new_post.id))

    return render_template("ask.html", form=form)


@api.route('/q/<int:id>', methods=['GET','POST'])
def question(id):

    question: Question = Question.query.filter(Question.id == id).first_or_404()
   
    question.views = question.views + 1 
    db.session.commit()   
    

    if current_user.is_authenticated:
        form: ResponceForm= ResponceForm()
        
        if form.validate_on_submit():
            body_md = (form.body.data[1:-1])
            parent =(form.parent.data)
            if not parent :
                parent = None

            new_response=Response(user_id=(current_user.id),question_id=id,date_posted=(datetime.now()),body=(body_md), parent_id=parent)
            db.session.add(new_response)
            db.session.commit()

        liked_by_user=False 
        for user in question.users_saved:
            if user.id == current_user.id:
                liked_by_user = True
        
    
        return render_template('question.html', question=question,liked_by_user=liked_by_user,form=form)
    else:
        return render_template('question.html', question=question)


@api.route('/r/<int:question_id>', methods=['POST'])
def get_responses(question_id):
    request_data = json.loads(request.data)

    responses: Response = Response.query.filter(Response.question_id == question_id, Response.parent_id == request_data['parent_id']).all()

    def liked_by_user(votes):
        if current_user.is_authenticated:
            for vote in votes:
                if vote.user_id == current_user.id:
                    return [True, vote.state]
        
        return [False,None]
    
    responses = [{
        "id" : response.id,
        'date_posted': response.date_posted, 
        'parent_id': response.parent_id, 
        'user_id':response.user.id,
        'username': response.user.username, 
        'question_id': response.question_id, 
        'body': response.body,
        "num_child": len(response.replies),
        "votes":sum([1 if vote.state else -1 for vote in response.votes]),
        "voted_by_user": liked_by_user(response.votes)
    } for response in responses]

    response = make_response(jsonify(responses), 200)
    response.headers["Content-Type"] = "application/json"
    return response



@api.route('/v/<int:response_id>/<int:state>', methods=['POST'])
@login_required
def handle_response(response,state):
    print(response)
    print(state)
