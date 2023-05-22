import secrets

DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = secrets.token_urlsafe(32)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///AskIT.db"
