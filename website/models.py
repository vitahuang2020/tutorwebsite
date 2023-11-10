from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    subject = db.Column(db.String(150))
    parent_email = db.Column(db.String(150))

class Pairs(db.Model, UserMixin):
    tutor_id = db.Column(db.Integer, primary_key=True) # to add foreign key constrain
    tutee_id = db.Column(db.Integer, primary_key=True) # to add foreign key constrain
    # tutor = db.Column(db.String(50))
    # tutor_email = db.Column(db.String(50))
    # tutee = db.Column(db.String(50))
    # tutee_email = db.Column(db.String(50))


