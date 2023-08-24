# imports
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from extentions import db
from forms import AskForm, ResponceForm
from models import User, Subject, Question, Response
from flask_login import current_user, login_required


# bluprint
home = Blueprint('home', __name__)


# route for the home page
@home.get('/')
def home_page():
    subjects = Subject.query.all()
    return render_template("home.html", subjects=subjects)


# User page
@home.route('/u/<int:id>')
def user(id):
    user = User.query.filter(User.id == id).first_or_404()
    return render_template("user.html", user=user)


# ask page
@home.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    # Make form object & set choices for subject
    form = AskForm()

    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]

    # validate form and question object
    if form.validate_on_submit():

        body_md = (form.body.data[1:-1])
        new_post = Question(user_id=(current_user.id),
                            subject_id=(form.subject.data),
                            title=(form.title.data),
                            date_posted=(datetime.now()),
                            body=(body_md),
                            views=0)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('home.question', id=new_post.id))

    return render_template("ask.html", form=form)


# Question route
@home.route('/q/<int:id>', methods=['GET', 'POST'])
def question(id):
    # get question and update view count.
    question: Question = Question.query.filter(
        Question.id == id).first_or_404()
    question.views = question.views + 1
    db.session.commit()

    if current_user.is_authenticated:
        # create response form and add response to db.
        form: ResponceForm = ResponceForm()

        if form.validate_on_submit():
            body_md = (form.body.data[1:-1])
            parent = (form.parent.data)
            if not parent:
                parent = None

            new_response = Response(user_id=(current_user.id),
                                    question_id=id,
                                    date_posted=(datetime.now()),
                                    body=(body_md),
                                    parent_id=parent)
            db.session.add(new_response)
            db.session.commit()
        # check if user has liked
        if question in current_user.saved:
            liked_by_user = True
        else:
            liked_by_user = False

        return render_template('question.html',
                               question=question,
                               liked_by_user=liked_by_user,
                               form=form)
    else:
        return render_template('question.html',
                               question=question)


# subject route
@home.route('/s/<subject>')
def subject(subject):
    # db query for subject
    subject = Subject.query.filter(
        Subject.name == (subject.capitalize())).first_or_404()
    return render_template('subject.html', subject=subject)
