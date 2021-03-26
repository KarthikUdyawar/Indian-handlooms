from flask import Blueprint, render_template, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User #, Profile
from . import db
import re

views = Blueprint('views',__name__)

@views.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'POST':  #  and 'cName' in request.form and 'firstName' in request.form and 'contact' in request.form and 'state' in request.form and 'address' in request.form and 'address' in request.form
        cName = request.form.get('cName')
        firstName = request.form.get('firstName')
        contact = request.form.get('contact')
        state = request.form.get('state')
        address = request.form.get('address')
        desc = request.form.get('desc')

        if cName == '':
            cName = User.company_Name
        elif len(cName) < 3:
            flash('Company Name must be at least 3 characters.', category='error')
            cName = User.company_Name
            
        if firstName == '':
            firstName = User.first_name
        elif len(firstName) < 3:
            flash('First Name must be at least 3 characters.', category='error')
            firstName = User.first_name
        
        if contact == '':
            contact = User.contact
        elif not re.match('^[0-9]*$', contact) or len(contact) > 10:                            #! This is meaningless
            flash('Contact must be at 10 digits.', category='error')
            contact = User.contact
        
        if state == 'None':
            state = User.state
            
        if address == '':
            address = User.address
        elif len(address) < 3:
            flash('Address must be at least 3 characters.', category='error')
            address = User.address
            
        if desc == '':
            desc = User.description
        elif len(desc) < 3:
            flash('Description must be at least 3 characters.', category='error')
            desc = User.description

        # if len(cName) < 3:
        #     flash('Company Name must be at least 3 characters.', category='error')
        # if len(firstName) < 3:
        #     flash('First Name must be at least 3 characters.', category='error')
        # if len(contact) < 10 or contact.isdigit():
        #     flash('Contact must be at 10 digits.', category='error')
        
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
        #     new_profile = User(company_Name = cName, contact = contact, description=desc)
        #     db.session.add(new_profile)
        
        user = User.query.get(current_user.id)
        user.company_Name = cName
        user.first_name = firstName
        user.contact = contact
        user.state = state
        user.address = address
        user.description = desc
        user.email = current_user.email
        user.password = current_user.password
        
        # newprofile = User(first_name=firstName, contact=contact, company_Name=cName, state=state, address=address, description=desc, email=current_user.email, password=current_user.password)
        # db.session.add(newprofile)
        
        db.session.commit()
        flash('Profile edited!',category='success')
        
    return render_template("profile.html", user=current_user)