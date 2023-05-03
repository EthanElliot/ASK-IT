from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


#DATABASE
db = SQLAlchemy()
DB_NAME = 'AskIT.db'


#FLASK LOGIN
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, )
    app.config.from_pyfile("../config.py") 

    #DATABASE CONFIG
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .models import UserSubject,Save,Vote,User,Subject,Question,Response

    #FLASK LOGIN CONFIG
    @login_manager.user_loader
    def load_user(user_id):
        # we use the primary key from our user table
        return User.query.get(int(user_id))

    # configue login user
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)



    from .auth import auth
    from .home import home
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
