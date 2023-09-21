'''this is the extentions file'''
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# DATABASE
db = SQLAlchemy()

# FLASK LOGIN
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    '''we use the primary key from our user table'''
    from models import User  # type: ignore
    return User.query.get(int(user_id))


login_manager.login_view = 'auth.signin'  # type: ignore


def is_big_int(number):
    '''big int check function'''
    if not number.bit_length() <= 63:
        return False
    else:
        return True
