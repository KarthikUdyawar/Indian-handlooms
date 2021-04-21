from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Contact
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import and_

auth = Blueprint('auth',__name__)

# @auth.route('/')
# def home():
#     return render_template("home.html", user=current_user)

@auth.route('/about')
def about():
    return render_template("about.html", user=current_user)

@auth.route('/')
def index():
    return render_template("index.html", user=current_user)

@auth.route('/east')
def east():
    return render_template("east.html", user=current_user)

@auth.route('/west')
def west():
    return render_template("west.html", user=current_user)

@auth.route('/north')
def north():
    return render_template("north.html", user=current_user)

@auth.route('/northeast')
def northeast():
    return render_template("northeast.html", user=current_user)

@auth.route('/central')
def central():
    return render_template("central.html", user=current_user)

@auth.route('/south')
def south():
    return render_template("south.html", user=current_user)

@auth.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':  
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        cName = request.form.get('cName')
        message = request.form.get('message')
        
        feedback = Contact(name=name, email=email, contact=contact, company_Name=cName, message=message)
        db.session.add(feedback)
        db.session.commit()
        
    return render_template("contact.html", user=current_user)

@auth.route('/database')
def database():
    return render_template("database.html", user=current_user)

@auth.route('/state/<state_name>', methods=['GET','POST'])
def state(state_name):
    state_select = User.query.filter_by(state = state_name)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        pname = User.query.filter(and_(User.state == state_name,User.product_name.like(search)))
        return render_template('state.html', user=pname, tag=tag, title=state_name)
    return render_template("state.html", user=state_select, title=state_name)

@auth.route('/state/<state_name>/info/<id>', methods=['GET','POST'])
def info(state_name,id):
    return render_template("info.html", user=User.query.filter_by(id = id) , title=id)

@auth.route('/login', methods=['GET','POST'])
def login(): 
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email == "admin@mail.com" and password == "admin123":
            return redirect(url_for('views.admin'))
        else:
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
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1,method='sha256'), contact='None', company_Name='None', state='None', address='None', product_name='None', description='None', image='website/static/images/profile/00default.png')
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