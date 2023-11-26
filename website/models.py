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
    subject1 = db.Column(db.String(150))
    subject2 = db.Column(db.String(150))
    subject3 = db.Column(db.String(150))
    subject4 = db.Column(db.String(150))
    subject5 = db.Column(db.String(150))

    parent_email = db.Column(db.String(150))

class Pairs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer) # to add foreign key constrain
    tutee_id = db.Column(db.Integer) # to add foreign key constrain
    subject = db.Column(db.String(150))

class Hours(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Integer)
    tutor_id = db.Column(db.Integer)
    time = db.Column(db.DateTime(timezone=True), default=func.now())


