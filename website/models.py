from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.String(50))
    grade = db.Column(db.Integer)
    subjects = db.Column(db.String(150))

    notes = db.relationship('Note')

class Pairs(db.Model, UserMixin):
    tutor = db.Column(db.String(50))
    tutor_email = db.Column(db.String(50))
    tutee = db.Column(db.String(50))
    tutee_email = db.Column(db.String(50))




