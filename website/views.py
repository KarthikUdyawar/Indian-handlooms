from flask import Blueprint, render_template, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User #, Profile
from . import db

views = Blueprint('views',__name__)

@views.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'POST':
        cName = request.form.get('cName')
        firstName = request.form.get('firstName')
        email = request.form.get('email')
        contact = request.form.get('contact')
        desc = request.form.get('desc')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be at least 3 characters.',category='error')
        elif len(firstName) < 2:
            flash('First name must be at least 2 characters.',category='error')
        elif password1 != password2:
            flash('Password does not match.',category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.',category='error')
        elif len(cName) < 2:
            flash('First name must be at least 2 characters.',category='error')
        elif len(contact) != 10:
            flash('Contact number must be 10 digits.',category='error')
        else:
            # new_profile = User(company_Name = cName, contact = contact, description=desc)
            # db.session.add(new_profile)
            user = User.query.get(current_user.id)
            user.company_Name = cName
            user.first_name = firstName
            user.email = email
            user.contact = contact
            user.description = desc
            user.password = generate_password_hash(password1,method='sha256')
            db.session.commit()
            flash('Profile edited!.',category='success')
        
    return render_template("profile.html", user=current_user)