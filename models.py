# imports
from extentions import db
from flask_login import UserMixin


# user subject for relationship
UserSubject = db.Table("UserSubject",
                       db.Column('user_id', db.Integer, db.ForeignKey(
                           'User.id'), primary_key=True),
                       db.Column('subject_id', db.Integer, db.ForeignKey(
                           'subject.id'), primary_key=True)
                       )


# save table for relationship
Save = db.Table("Save",
                db.Column('question_id', db.Integer, db.ForeignKey(
                    'question.id'), primary_key=True),
                db.Column('user_id', db.Integer, db.ForeignKey(
                    'User.id'), primary_key=True)
                )


# association object table for vote
class Vote(db.Model):
    __tablename__ = "Vote"

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    response_id = db.Column(db.Integer, db.ForeignKey('response.id'))
    state = db.Column(db.Boolean, nullable=False)
    db.PrimaryKeyConstraint(user_id, response_id)

    user = db.relationship("User", backref="votes")
    response = db.relationship("Response", backref="votes")

# https://stackoverflow.com/questions/24872541/could-not-assemble-any-primary-key-columns-for-mapped-table


# User table database model
class User(db.Model, UserMixin):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)

    saved = db.relationship('Question', secondary=Save, backref="users_saved")


# subject model
class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    users = db.relationship('User', secondary=UserSubject, backref="subjects")


# question model
class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    title = db.Column(db.String(), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.String(), nullable=False)
    views = db.Column(db.Integer())

    user = db.relationship('User', backref='questions')
    subject = db.relationship('Subject', backref='questions')

# response model


class Response(db.Model):
    __tablename__ = "response"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    date_posted = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.String(), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('response.id'))

    user = db.relationship('User', backref='responses')
    question = db.relationship('Question', backref='responses')
    replies = db.relationship('Response', backref=db.backref(
        'parent', remote_side=[id]), lazy='joined')
