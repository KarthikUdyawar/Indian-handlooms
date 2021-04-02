from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    company_Name = db.Column(db.String(150))
    contact = db.Column(db.String(10)) 
    description = db.Column(db.String(500))
    state = db.Column(db.String(20))
    address = db.Column(db.String(200))
    image = db.Column(db.String(200))
    product_name = db.Column(db.String(100))