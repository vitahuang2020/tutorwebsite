from flask import Blueprint, render_template, flash, request, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Pairs, Hours
from . import db
from sqlalchemy.orm import aliased
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST']) # homepage
@login_required
def home(tutor_id=None):
    tutors = User.query.filter_by(role=2).all()
    tutees = User.query.filter_by(role=1).all()

    UserTutor = aliased(User)
    UserTutee = aliased(User)


    # pairs_list = (Pairs.query.join(User, User.id == Pairs.tutor_id)
    #         .join(User, User.id == Pairs.tutee_id)
    #          .add_columns(Pairs.tutor_id, User.first_name, User.last_name, Pairs.tutee_id, User.first_name, User.last_name)).all()

    pairs_list = (Pairs.query
                  .join(UserTutor, UserTutor.id == Pairs.tutor_id)
                  .join(UserTutee, UserTutee.id == Pairs.tutee_id)
                  .add_columns(
        Pairs.tutor_id,
        UserTutor.first_name.label("tutor_first_name"),
        UserTutor.last_name.label("tutor_last_name"),
        Pairs.tutee_id,
        Pairs.id,
        UserTutee.first_name.label("tutee_first_name"),
        UserTutee.last_name.label("tutee_last_name")
    ).all())

    unpairs_list = (Pairs.query.filter_by(tutor_id=0)
                  .join(UserTutee, UserTutee.id == Pairs.tutee_id)
                  .add_columns(
        Pairs.id,
        Pairs.subject,
        UserTutee.email.label("tutee_email"),
        UserTutee.first_name.label("tutee_first_name"),
        UserTutee.last_name.label("tutee_last_name"),
        UserTutee.grade.label("tutee_grade"),
    ).all())

    print(pairs_list)

    print(tutors)
    if request.method == 'GET':
        print("Get request on home page.")
        print(len(tutors))
        return render_template("home.html", user=current_user, tutors=tutors, tutees=tutees, pairs_list=pairs_list, unpairs_list=unpairs_list)

@views.route('/unpair', methods=['POST'])
def unpair():
    data = request.get_json()
    data_id = data['Id']
    pair = Pairs.query.get(data_id)
    if pair:
        pair.tutor_id = 0
        db.session.commit()
        return jsonify({"message": "Unpaired successfully"}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

@views.route('/hours', methods=['POST']) # homepage
@login_required
def hours():
    if request.method == 'POST':
        hours = request.form.get("hours")
        new_hours = Hours(hours=hours, tutor_id=current_user.id)

        db.session.add(new_hours)
        db.session.commit()
        flash('Hours logged in', category='success')

    return(render_template("hours.html", user=current_user))

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selected_time = db.Column(db.String(10), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

@views.route('/')
def index():
    times = TimeEntry.query.all()
    return render_template('index.html', times=times)

@views.route('/add', methods=['POST'])
def add_time():
    selected_time = request.form.get('selected_time')
    new_entry = TimeEntry(selected_time=selected_time)
    db.session.add(new_entry)
    db.session.commit()