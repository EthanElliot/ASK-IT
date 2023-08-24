# imports
from flask import Flask, render_template
from extentions import db, login_manager
from home import home
from auth import auth
from api import api
from werkzeug.exceptions import HTTPException


# FLASK APP
app = Flask(__name__)
app.config.from_pyfile("./config.py")

# init db
db.init_app(app)
login_manager.init_app(app)

# register bluprints
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(api)


# general error handeler
@app.errorhandler(HTTPException)
def handle_exception(e):
    # generate response
    response = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }

    return render_template(
        'error.html',
        response=response
    )


# run app
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
