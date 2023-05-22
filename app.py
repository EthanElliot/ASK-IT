from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app= Flask(__name__)
app.config.from_pyfile("./config.py") 


#DATABASE
db = SQLAlchemy(app)
from models import *

#FLASK LOGIN
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    # we use the primary key from our user table
    return User.query.get(int(user_id))

login_manager.login_view = 'auth.signin'


if __name__ == "__main__":
    app.run(debug=True, port=5000)