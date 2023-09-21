'''this is the routes for the home pages'''
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, abort
from forms import AskForm, ResponseForm
from models import User, Subject, Question, Response
from flask_login import current_user, login_required
from extentions import db, is_big_int


# bluprint
home = Blueprint('home', __name__)


# route for the home page
@home.get('/')
def home_page():
    '''home page for displayingr routes'''
    subjects = Subject.query.all()
    return render_template("home.html", subjects=subjects)


# User page
@home.route('/u/<int:user_id>')
def user(user_id):
    '''user page for displaying user info'''
    # id check
    if not is_big_int(user_id):
        abort(404)

    userdata = User.query.filter(User.id == user_id).first_or_404()
    return render_template("user.html", user=userdata)


# ask page
@home.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    '''ask route for users asking a question'''
    # Make form object & set choices for subject
    form = AskForm()

    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]

    # validate form and question object
    if form.validate_on_submit():

        body_md = form.body.data[1:-1]
        new_post = Question(user_id=(current_user.id),
                            subject_id=(form.subject.data),
                            title=(form.title.data),
                            date_posted=(datetime.now()),
                            body=(body_md),
                            views=0)
        db.session.add(new_post)  # type: ignore
        db.session.commit()  # type: ignore

        return redirect(url_for('home.question', question_id=new_post.id))

    return render_template("ask.html", form=form)


# Question route
@home.route('/q/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    '''question route for showing questions'''
    # big int check
    if not is_big_int(question_id):
        abort(404)
    # get questiondata and update view count.
    questiondata: Question = Question.query.filter(
        Question.id == question_id).first_or_404()
    questiondata.views = questiondata.views + 1
    db.session.commit()  # type: ignore

    if current_user.is_authenticated:  # type: ignore
        # create response form and add response to db.
        form: ResponseForm = ResponseForm()

        if form.validate_on_submit():
            body_md = form.body.data[1:-1]
            parent = form.parent.data
            if not parent:
                parent = None

            new_response = Response(user_id=(current_user.id),  # type: ignore
                                    question_id=question_id,
                                    date_posted=(datetime.now()),
                                    body=(body_md),
                                    parent_id=parent)
            db.session.add(new_response)  # type: ignore
            db.session.commit()  # type: ignore
        # check if user has liked
        if questiondata in current_user.saved:  # type: ignore
            liked_by_user = True
        else:
            liked_by_user = False

        return render_template('question.html',
                               question=questiondata,
                               liked_by_user=liked_by_user,
                               form=form)
    else:
        return render_template('question.html',
                               question=questiondata)


# subject route
@home.route('/s/<subject_name>')
def subject(subject_name):
    '''subject route'''
    # db query for subject
    subjectdata = Subject.query.filter(
        Subject.name == (subject_name.capitalize())).first_or_404()
    return render_template('subject.html', subject=subjectdata)
