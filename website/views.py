from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import User, Pairs, Hours
from . import db
from sqlalchemy.orm import aliased
from datetime import datetime
from .util import Utils

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
        Pairs.subject,
        UserTutee.first_name.label("tutee_first_name"),
        UserTutee.last_name.label("tutee_last_name")
    ).all())

    unpairs_list = (Pairs.query.filter_by(tutor_id=0)
                  .join(UserTutee, UserTutee.id == Pairs.tutee_id)
                  .add_columns(
        Pairs.id,
        Pairs.tutee_id,
        Pairs.subject,
        UserTutee.email.label("tutee_email"),
        UserTutee.teacher_email.label("tutee_teacher_email"),
        UserTutee.first_name.label("tutee_first_name"),
        UserTutee.last_name.label("tutee_last_name"),
        UserTutee.grade.label("tutee_grade"),
    ).all())

    print("Unpaired: ")
    print(unpairs_list)

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
        # Save tutor_id and tutee_id before setting tutor_id to 0
        tutor_id = pair.tutor_id
        tutee_id = pair.tutee_id

        pair.tutor_id = 0
        db.session.commit()

        tutors = User.query.filter_by(id=tutor_id).all()
        tutees = User.query.filter_by(id=tutee_id).all()

        if tutors and tutees:
            u = Utils()
            u.send_mail(tutors[0].email,
                        'Branksome Hall Tutor Club',
                        'This email is to inform you that you are no longer paired up with tutee: ' + tutees[0].first_name + ' ' +
                        tutees[0].last_name + '. Please wait until you are paired up with another student.')

            u.send_mail(tutees[0].email,
                        'Branksome Hall Tutor Club',
                        'This email is to inform you that you are no longer paired up with tutor: ' + tutors[0].first_name + ' ' +
                        tutors[0].last_name + '. If you would still like tutoring in this subject, please let Ms. Contreras and Ms. Blyth know.')

            db.session.close()

            return jsonify({"message": "Unpaired successfully"}), 200
        else:
            return jsonify({"error": "Invalid user data"}), 400
    else:
        return jsonify({"error": "Invalid data"}), 400


@views.route('/hours', methods=['GET', 'POST'])
@login_required
def hours():
    # Fetch and display time entries
    times = Hours.query.filter_by(tutor_id=current_user.id).all()

    if request.method == 'POST':
        selected_time = int(request.form.get('selected_time'))
        note = request.form.get('notes')
        print(note)
        # Calculate the hours based on the selected time
        hours_logged = selected_time

        new_hour = Hours(hours=hours_logged, note=note, tutor_id=current_user.id, time=datetime.utcnow())
        db.session.add(new_hour)
        db.session.commit()
        flash('Hours logged!', category='success')

    return render_template("hours.html", user=current_user, times=times)

@views.route('/delete_time/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_time(id):
    # Implement logic to delete the time entry with the specified ID
    time_entry = Hours.query.get(id)
    if time_entry:
        db.session.delete(time_entry)
        db.session.commit()
        flash('Time entry deleted!', category='success')
    else:
        flash('Time entry not found.', category='danger')

    # Render the 'hours.html' template after deletion
    return render_template('hours.html', user=current_user, times=Hours.query.filter_by(tutor_id=current_user.id).all())

@views.route('/tutee_page', methods=['GET','POST'])
@login_required
def tutee_page():
    return render_template("tutee_page.html", user=current_user)

@views.route('/training', methods=['GET','POST'])
@login_required
def training():
    return render_template("training.html", user=current_user)

@views.route('/delete_user/<string:user_type>/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_type, user_id):
    user = None

    if user_type == 'tutor':
        user = User.query.filter_by(id=user_id, role=2).first()
    elif user_type == 'tutee':
        user = User.query.filter_by(id=user_id, role=1).first()

    print(user_type, user_id, user)  # Debugging line

    if user:
        db.session.delete(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Rollback changes if an exception occurs
            print(f"Error committing changes: {str(e)}")

        # Send notification email to the user
        u = Utils()
        u.send_mail(user.email,
                    'Branksome Hall Tutor Club',
                    'This email is to inform you that your account has been deleted from the Branksome Hall Tutor Program.')

        flash('User deleted!', category='success')
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "error": "Invalid user type or ID"}), 400

    @views.route('/tutor_hours/<int:tutor_id>', methods=['GET'])
    @login_required
    def tutor_hours(tutor_id):
        # Fetch and display time entries logged by the specified tutor
        times = Hours.query.filter_by(tutor_id=tutor_id).all()

        return render_template("tutor_hours.html", user=current_user, times=times)

@views.route('/tutor_hours/<int:tutor_id>')
@login_required
def tutor_hours(tutor_id):
    tutor = User.query.get_or_404(tutor_id)
    times = Hours.query.filter_by(tutor_id=tutor_id).all()
    return render_template("tutor_hours.html", user=current_user, tutor=tutor, times=times)