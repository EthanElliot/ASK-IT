# imports
from flask import Blueprint, redirect, url_for,\
    make_response, jsonify, abort, request
from extentions import db
from models import Subject, Question, Response, Vote
from flask_login import current_user, login_required
import json
from sqlalchemy import desc, asc


# bluprint
api = Blueprint('api', __name__)


# route for get responses
@api.route('/get_responses/<int:question_id>', methods=['POST'])
def get_responses(question_id):

    if not request.data:
        abort(400)
    # get data send from request
    request_data = json.loads(request.data)

    # get response
    responses: Response = Response.query.filter(
        Response.question_id == question_id,
        Response.parent_id == request_data['parent_id']
    ).all()

    # function for liked by user (used recursively)
    def liked_by_user(votes):
        if current_user.is_authenticated:
            for vote in votes:
                if vote.user_id == current_user.id:
                    return [True, vote.state]

            return [True, None]

        return [False, None]

    # create response for reply
    responses = [{
        "id": response.id,
        'date_posted': response.date_posted,
        'parent_id': response.parent_id,
        'user_id': response.user.id,
        'username': response.user.username,
        'question_id': response.question_id,
        'body': response.body,
        "num_child": len(response.replies),
        "sum_votes": sum([1 if vote.state else -1 for vote in response.votes]),
        "voted_by_user": liked_by_user(response.votes),
        "votes":len(response.votes)
    } for response in responses]

    response = make_response(jsonify(responses), 200)
    response.headers["Content-Type"] = "application/json"
    return response


# route for update vote
@api.route('/update_vote/<int:response_id>', methods=['POST'])
@login_required
def update_vote(response_id):
    if not request.data:
        abort(400)
    request_data = json.loads(request.data)

    vote = Vote.query.filter(
        Vote.user_id == current_user.id,
        Vote.response_id == response_id
    ).first()

    # add new vote if none present
    if not vote:
        new_vote = Vote(user_id=current_user.id,
                        response_id=response_id, state=request_data)
        db.session.add(new_vote)
        db.session.commit()
        if request_data:
            delta = 1
        else:
            delta = -1
        state = new_vote.state
    # if there is a vote and the user had alreaded voted that way remove vote.
    elif vote and vote.state == request_data:
        db.session.delete(vote)
        db.session.commit()
        if request_data:
            delta = -1
        else:
            delta = 1
        state = None

    # if there is a vote and the user has voted the other way change vote.
    elif vote and vote.state != request_data:
        if vote.state == 0:
            vote.state = 1
            delta = 2
            state = True
        elif vote.state == 1:
            vote.state = 0
            delta = -2
            state = False
        db.session.commit()

    print(state)

    response = make_response(jsonify({'delta': delta, 'state': state}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/update_Save_Status/<int:question_id>')
@login_required
def update_Save_Status(question_id):
    question = Question.query.filter(Question.id == question_id).first_or_404()
    user = current_user
    if question in user.saved:
        user.saved.remove(question)
    else:
        user.saved.append(question)
    db.session.commit()
    return redirect(url_for('home.question', question_id=question_id))


# get questions
@api.route('/get_questions', methods=['POST'])
def get_questions():
    '''get questions'''

    # type check count
    try:
        counter = int(request.args.get("count"))
    except ValueError:
        abort(400)

    user_id = request.args.get("user_id")
    subject_id = request.args.get("subject_id")
    filter = request.args.get("filter")

    order_direction = request.args.get("order_direction")
    order_by = request.args.get("order_by")

    # set order by
    if order_by == 'date' and order_direction == 'desc':
        order = desc(Question.date_posted)
    elif order_by == 'date' and order_direction == 'asc':
        order = asc(Question.date_posted)
    elif order_by == 'viewed' and order_direction == 'desc':
        order = desc(Question.views)
    elif order_by == 'viewed' and order_direction == 'asc':
        order = asc(Question.views)
    else:
        abort(400)

    # do query
    query: Question = Question.query.order_by(order)

    # add filters
    if user_id:
        query = query.filter(Question.user_id == user_id)

    if filter:
        query = query.filter(Question.title.ilike(f'%{filter}%'))

    if subject_id:
        query = query.filter(Question.subject_id == subject_id)

    questions = query.offset(counter).limit(5).all()

    # genereate reply
    questions = [{
        "id": question.id,
        "title": question.title,
        "user_id": question.user_id,
        "user_username": question.user.username,
        "date_posted": question.date_posted,
        "body": question.body,
        "views": question.views,
        "subject": question.subject.name,
        "saves": len(question.users_saved)
    } for question in questions]

    return make_response(jsonify(questions), 200)


# follow reply route
@api.route('/follow_subject/<int:subject_id>')
@login_required
def follow_subject(subject_id):
    # subject query
    subject = Subject.query.filter(Subject.id == subject_id).first_or_404()
    user = current_user

    # update save status
    if subject in user.subjects:
        user.subjects.remove(subject)
    else:
        user.subjects.append(subject)
    db.session.commit()
    return redirect(url_for('home.subject', subject_name=subject.name))
