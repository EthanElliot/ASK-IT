from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import User

app= Flask(__name__)
app.config.from_pyfile("./config.py") 


#DATABASE
db = SQLAlchemy()
DB_NAME = 'AskIT.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


#FLASK LOGIN
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # we use the primary key from our user table
    return User.query.get(int(user_id))

login_manager.login_view = 'auth.signin'


if __name__ == "__main__":
    app.run()