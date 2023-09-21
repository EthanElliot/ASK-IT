'''form classes'''
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField,\
    ValidationError, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, Email
import html2text
from models import User


# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def alphabet_check(form, field):
    '''char check'''
    for char in field.data:
        if char not in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_"]:
            raise ValidationError(f'"{char}" is not allowed.')
        else:
            continue


def username_taken(form, field):
    '''username check'''
    if field.type != "StringField":
        return
    else:
        user = User.query.filter((User.username == field.data)).first()

        if user:
            raise ValidationError('username already taken')


def email_taken(form, field):
    '''email check'''
    if field.type != "EmailField":
        return
    else:
        user = User.query.filter((User.email == str(field.data))).first()
        if user:
            raise ValidationError('email already taken')


class SignUpForm(FlaskForm):
    '''signup form'''
    username = StringField(
        'username',
        validators=[
            DataRequired(message="username is required"),
            Length(min=4, max=50),
            alphabet_check,
            username_taken],
        render_kw={
            "placeholder": "username"}
    )

    email = EmailField(
        'email',
        validators=[
            Email(),
            DataRequired(message="username is required"),
            email_taken],
        render_kw={
            "placeholder": "email"}
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=3)
        ],
        render_kw={"placeholder": "Password"})

    confirm = PasswordField(
        'Verify password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={"placeholder": "Verify password"})

    submit = SubmitField('sign up')


class SignInForm(FlaskForm):
    '''signin form'''
    identifier = StringField(
        'identifier',
        validators=[
            DataRequired(message="username or password is required"),
            Length(min=4, max=50)],
        render_kw={
            "placeholder": "username or email"}
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=3)
        ],
        render_kw={"placeholder": "Password"})

    submit = SubmitField('sign in')


# Ask form object
class AskForm(FlaskForm):
    '''ask form'''
    title = StringField('title',
                        validators=[
                            DataRequired(message='post must have a title'),
                            Length(min=15, max=100)],
                        render_kw={"placeholder": "e.g. what is 1+1?"})
    subject = SelectField(choices=[])

    body = HiddenField('body', validators=[])
    submit = SubmitField("Ask")
    # min lenth validator

    def validate_body(self, body):
        text = len(html2text.html2text(body.data))
        if text < 40:
            raise ValidationError('body of question is too short')

        if text > 2000:
            raise ValidationError('body of question is too long')


class ResponseForm(FlaskForm):
    '''response form'''
    # min lenth validator
    body = HiddenField('body', validators=[])
    parent = HiddenField('parent')
    submit = SubmitField("submit")

    def validate_body(self, body):
        text = len(html2text.html2text(body.data))
        if text < 20:
            raise ValidationError('body of response too short')

        if text > 1000:
            raise ValidationError('body of response too long')
