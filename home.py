from flask import Blueprint, render_template


api = Blueprint('', __name__)


@api.get('/')
def home():
    return render_template("home.html")
