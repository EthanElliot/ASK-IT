from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DB_NAME = 'AskIT.db'

   


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py") 

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .models import UserSubject,Save,Vote,User,Subject,Question,Response



    from .home import home
    app.register_blueprint(home, url_prefix='/')

    return app
