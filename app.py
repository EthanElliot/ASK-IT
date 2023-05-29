from flask import Flask
from extentions import db,login_manager
from home import api

#FLASK APP
app= Flask(__name__)
app.config.from_pyfile("./config.py") 

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True, port=5000)