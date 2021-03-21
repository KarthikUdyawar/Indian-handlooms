from flask import Blueprint, render_template

auth = Blueprint('auth',__name__)

@auth.route('/about')
def about():
    return render_template("about.html")

@auth.route('/database')
def database():
    return render_template("database.html")

@auth.route('/login')
def login(): 
    return render_template("login.html")

@auth.route('/sign-up')
def sign_up():
    return render_template("signUp.html")

@auth.route('/logout')
def logout():
    return '<h3>Logout</h3>'
