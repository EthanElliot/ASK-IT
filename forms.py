from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField,ValidationError, SelectField,HiddenField,FileField
from wtforms.validators import DataRequired, Length, EqualTo
from models import Subject, User
from extentions import db
import logging
import html2text
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)



#alphabet validator
def alphabet_check(form, field):
    for char in field.data:
        if char not in ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","_"]:
            raise ValidationError(f'"{char}" is not allowed.')
        else:
            continue


def username_taken(form, field):
    if field.type != "StringField":
        return
    else: 
        user = User.query.filter((User.username == field.data)).first()
        
        if user:
            raise ValidationError('username already taken')


def email_taken(form, field):
    if field.type != "EmailField":
        return
    else: 
        user = User.query.filter((User.email == str(field.data))).first()
        if user:
            raise ValidationError('email already taken')

#form classea
class SignUpForm(FlaskForm):
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

#add must select validator
class AskForm(FlaskForm):
    title = StringField('title', 
    validators=[
        DataRequired(message='post must have a title'),
        Length(min=15, max=100)], render_kw={"placeholder": "e.g. what is 1+1?"})
    subject = SelectField(choices=[])

    body= HiddenField('body', validators=[])
    submit = SubmitField("Ask")
    #min lenth validator
    def validate_body(self, body):
        text = len(html2text.html2text(body.data))
        if text < 40:
            raise ValidationError('body of question is too short')    

        if text > 2000:
            raise ValidationError('body of question is too long')


class ResponceForm(FlaskForm):
    #min lenth validator
    body= HiddenField('body', validators=[])
    parent=HiddenField('parent')
    submit = SubmitField("submit")
    
    def validate_body(self, body):
        text = len(html2text.html2text(body.data))
        if text < 20:
            raise ValidationError('body of question too short')    

        if text > 1000:
            raise ValidationError('body of question too long')

