from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField,ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from .models import User


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