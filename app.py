'''this is the app file to init modules and run app'''
# imports
from flask import Flask, render_template, abort
from flask_login import current_user
from werkzeug.exceptions import HTTPException
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from extentions import db, login_manager
from home import home
from auth import auth
from api import api
from models import Subject, Question, Response, User, Vote


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


class MyAdminIndexView(AdminIndexView):
    '''init admin index and make it hidden to non admin users'''

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        # Redirect non-admin users to a 404 page
        abort(404)

    def is_visible(self):
        # This view won't appear in the menu structure
        return False


class AdminModelView(ModelView):
    '''init admin models and make it hidden to non admin users'''

    def is_accessible(self):
        if current_user.is_authenticated and current_user.admin:
            return True
        else:
            abort(404)


admin = Admin(app,  index_view=MyAdminIndexView())
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Question, db.session))
admin.add_view(AdminModelView(Response, db.session))
admin.add_view(AdminModelView(Subject, db.session))
admin.add_view(AdminModelView(Vote, db.session))


@app.errorhandler(HTTPException)
def handle_exception(e):
    '''general error handeler for HTTP errors only'''
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
