import secrets


DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = secrets.token_urlsafe(32)
