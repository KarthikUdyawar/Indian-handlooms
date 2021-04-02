from flask import Blueprint, render_template, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import User 
from . import db
import os

views = Blueprint('views',__name__)

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in ["JPEG", "JPG", "PNG", "GIF"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):
    if int(filesize) <= 0.5 * 1024 * 1024:
        return True
    else:
        return False

@views.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'POST':  
        cName = request.form.get('cName')
        firstName = request.form.get('firstName')
        contact = request.form.get('contact')
        state = request.form.get('state')
        address = request.form.get('address')
        pName = request.form.get('pName')
        desc = request.form.get('desc')
        path_image = request.form.get('image')

        if request.files:
            if "filesize" in request.cookies:
                image = request.files["image"]
                if image.filename == "":
                    path_image = User.image
                elif not allowed_image_filesize(request.cookies["filesize"]):
                    flash('Filesize exceeded maximum limit (500 Kb)', category='error')
                    path_image = User.image
                elif allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    path_image = os.path.join("website/static/images/profile/" , filename)
                    image.save(path_image)
                else:
                    flash('That file extension is not allowed', category='error')

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
        elif not (contact.isdigit() and len(contact) == 10):                            
            flash('Contact must be at 10 digits.', category='error')
            contact = User.contact
        
        if state == 'None':
            state = User.state
            
        if address == '':
            address = User.address
        elif len(address) < 3:
            flash('Address must be at least 3 characters.', category='error')
            address = User.address
            
        if pName == '':
            pName = User.product_name
        elif len(pName) < 3:
            flash('Product name must be at least 3 characters.', category='error')
            pName = User.product_name
            
        if desc == '':
            desc = User.description
        elif len(desc) < 3:
            flash('Description must be at least 3 characters.', category='error')
            desc = User.description
        
        user = User.query.get(current_user.id)
        user.company_Name = cName
        user.first_name = firstName
        user.contact = contact
        user.state = state
        user.address = address
        user.description = desc
        user.email = current_user.email
        user.password = current_user.password
        user.image = path_image
        user.product_name = pName
        
        db.session.commit()
        flash('Profile edited!',category='success')
        
    return render_template("profile.html", user=current_user)