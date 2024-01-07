from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

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
    teacher_email = db.Column(db.String(150))
    parent_email = db.Column(db.String(150))

class Pairs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer) # to add foreign key constrain
    tutee_id = db.Column(db.Integer) # to add foreign key constrain
    subject = db.Column(db.String(150))

class Hours(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Integer, nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    note = db.Column(db.String(512))

    # Add this property to format the time
    @property
    def formatted_time(self):
        return self.time.strftime("%Y-%m-%d")


