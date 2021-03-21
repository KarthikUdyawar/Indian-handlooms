from flask import Blueprint, render_template

auth = Blueprint('auth',__name__)

@auth.route('/about')
def login():
    return render_template("about.html")

@auth.route('/database')
def sign_up():
    return render_template("database.html")