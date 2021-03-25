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
        contact = request.form.get('contact')
        state = request.form.get('state')
        address = request.form.get('address')
        desc = request.form.get('desc')

        # if cName == '':
        #     cName = User.company_Name
        # elif firstName == '':
        #     firstName = User.first_name
        # elif contact == '':
        #     contact = User.contact
        # elif state == 'None':
        #     state = User.state
        # elif address == '':
        #     address = User.address
        # elif desc == '':
        #     desc = User.desc
        # else:
        #     pass
        
        # user = User.query.filter_by(email=email).first() 
        # if user and email != user.email:
        #     flash('Email already exists.', category='error')
        # elif len(email) < 4 and email != '':
        #     flash('Email must be at least 3 characters.',category='error')
        # elif len(firstName) < 2 and firstName != '':
        #     flash('First name must be at least 2 characters.',category='error')
        # elif password1 != password2:
        #     flash('Password does not match.',category='error')
        # elif len(password1) < 7 and password1 != '' and password2 != '':
        #     flash('Password must be at least 7 characters.',category='error')
        # elif len(cName) < 2:
        #     flash('First name must be at least 2 characters.',category='error')
        # elif len(contact) != 10 and contact != '':
        #     flash('Contact number must be 10 digits.',category='error')
        # else:
            # new_profile = User(company_Name = cName, contact = contact, description=desc)
            # db.session.add(new_profile)
        user = User.query.get(current_user.id)
        user.company_Name = cName
        user.first_name = firstName
        user.contact = contact
        user.state = state
        user.address = address
        user.description = desc
        db.session.commit()
        flash('Profile edited!.',category='success')
        
    return render_template("profile.html", user=current_user)