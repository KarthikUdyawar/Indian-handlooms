from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/')
def home():
    return render_template("home.html", user=current_user)

@auth.route('/about')
def about():
    return render_template("about.html", user=current_user)

@auth.route('/database')
def database():
    return render_template("database.html", user=current_user)

@auth.route('/login', methods=['GET','POST'])
def login(): 
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login successfully!',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password',category='error')
        else:
            flash('User does not exist!',category='error')
    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be at least 3 characters.',category='error')
        elif len(firstName) < 3:
            flash('First name must be at least 2 characters.',category='error')
        elif password1 != password2:
            flash('Password does not match.',category='error')
        elif len(password1) < 8:
            flash('Password must be at least 7 characters.',category='error')
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1,method='sha256'), contact='None', company_Name='None', state='None', address='None', description='None', image='website/static/images/profile/00default.png')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created!.',category='success')
            return redirect(url_for('views.profile'))
    return render_template("signUp.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
