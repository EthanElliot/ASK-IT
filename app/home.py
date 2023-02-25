from flask import Blueprint, render_template

home = Blueprint("home", __name__)


@home.route("/")
def hello():
    return "hello world."
