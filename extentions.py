from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


#DATABASE
db = SQLAlchemy()

#FLASK LOGIN
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    # we use the primary key from our user table
    from models import User
    return User.query.get(int(user_id))

login_manager.login_view = 'signin'

