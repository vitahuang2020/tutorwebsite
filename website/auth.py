from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Pairs
from werkzeug.security import generate_password_hash, check_password_hash
from.import db
from flask_login import login_user, login_required, logout_user, current_user
from .util import Utils

auth = Blueprint('auth', __name__)
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # new_user = User(email="admin@gmail.com", first_name="Admin", last_name="Admin",
        #                 password=generate_password_hash("123456", method='sha256'), role=3)
        # db.session.add(new_user)
        # db.session.commit()

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                # print(user.first_name)
                flash(user.first_name + ' is logged in successfully!', category='success')
                login_user(user, remember=True)
                if user.role == 1:
                    return redirect(url_for('views.tutee_page'))
                elif user.role == 2:
                    return redirect(url_for('auth.hours'))
                elif user.role == 3:
                    return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up_tutee', methods=['GET','POST'])
def sign_up_tutee():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = 1
        grade = request.form.get('grade')
        subject1 = request.form.get('subject1')
        subject2 = request.form.get('subject2')
        subject3 = request.form.get('subject3')
        subject4 = request.form.get('subject4')
        subject5 = request.form.get('subject5')
        teacher_email = request.form.get('teacher_email')
        parent_email = request.form.get('parent_email')
        user = User.query.filter_by(email=email).first()

        # no_option_form1 = request.form.get('flexRadioGroup1') == 'Nope'
        # no_option_form2 = request.form.get('flexRadioGroup2') == 'No'
        #
        # if no_option_form1 or no_option_form2:
        #     flash('You cannot sign up if you have selected "No" in either of the forms.', category='error')
        #     return render_template("sign_up_tutee.html", user=current_user)

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 5 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif len(subject1) < 1:
            flash('Please input a subject1 you would like to be tutored in', category='error')
        elif len(parent_email) < 1:
            flash('Please input your parent email', category='error')
        elif len(teacher_email) < 1:
            flash('Please input your teacher email', category='error')
        else:
            # add user to database

            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password1, method='sha256'),
                role=role,
                grade=grade,
                teacher_email=teacher_email,
                parent_email=parent_email,
                subject1=subject1,
                subject2=subject2,
                subject3=subject3,
                subject4=subject4,
                subject5=subject5
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            new_pairs = Pairs(tutee_id=current_user.id,tutor_id=0, subject=subject1)
            db.session.add(new_pairs)
            db.session.commit()

            if len(subject2) > 0:
                new_pairs = Pairs(tutee_id=current_user.id, tutor_id=0,subject=subject2)
                db.session.add(new_pairs)
                db.session.commit()

            if len(subject3) > 0:
                new_pairs = Pairs(tutee_id=current_user.id, tutor_id=0, subject=subject3)
                db.session.add(new_pairs)
                db.session.commit()

            if len(subject4) > 0:
                new_pairs = Pairs(tutee_id=current_user.id, tutor_id=0, subject=subject4)
                db.session.add(new_pairs)
                db.session.commit()

            if len(subject5) > 0:
                new_pairs = Pairs(tutee_id=current_user.id, tutor_id=0, subject=subject5)
                db.session.add(new_pairs)
                db.session.commit()

            u = Utils()
            u.send_mail(parent_email,
                        'Branksome Hall Tutor Club',
                        'This email is to inform you that your child, ' + first_name + ' ' + last_name + ', is signed up as a tutee for the Branksome Hall Tutor Program. If you have any questions, please directly contact Ms. Contreras or Ms. Blyth.')
            u.send_mail(email,
                        'Branksome Hall Tutor Club',
                        'This email is to inform you that you are signed up for the Branksome Hall Tutor Program!')

            flash('Account created!', category='success')
            print("account created")
            return redirect(url_for('views.tutee_page'))

    return render_template("sign_up_tutee.html", user=current_user)

@auth.route('/sign_up_tutor', methods=['GET','POST'])
def sign_up_tutor():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = 2
        grade = request.form.get('grade')
        subject = request.form.get('subject')
        teacher_email = request.form.get('teacher_email')
        parent_email = request.form.get('parent_email')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 5 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif len(subject) < 1:
            flash('Please input a subject you would like to tutor', category='error')
        elif len(parent_email) < 1:
            flash('Please input your parent email', category='error')
        elif len(teacher_email) < 1:
            flash('Please input your teacher email for a reference', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1,method='sha256'), role=role, grade=grade, parent_email=parent_email, subject1=subject, teacher_email=teacher_email)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            u = Utils()
            u.send_mail(parent_email,
                        'Branksome Hall Tutor Club',
                        'This email is to inform you that your child, ' + first_name + ' ' + last_name + ', is signed up as a tutor for the Branksome Hall Tutor Program. If you have any questions, please directly contact Ms. Contreras or Ms. Blyth.')
            u.send_mail(email,
                        'Branksome Hall Tutor Club',
                        'This email is to inform you that you are signed up for the Branksome Hall Tutor Program!')

            flash('Account created!', category='success')
            print("account created")
            return redirect(url_for('login.html'))

    return render_template("sign_up_tutor.html", user=current_user)

@auth.route('/flash_message', methods=['POST'])
def flash_message():
    data = request.get_json()

    # Extract message and category from the JSON data
    message = data.get('message')
    category = data.get('category', 'info')  # Default category is 'info'

    # Flash the message with the specified category
    flash(message, category='error')

    # Return a JSON response to acknowledge the receipt of the message
    return jsonify({'status': 'success'})

@auth.route('/pair', methods=['GET','POST'])
@login_required
def pair():
    print("in the pair() function")
    try:
        data = request.json  # Assuming you send the selected tutor and tutee data as JSON
        print(data)

        tutor_id = data.get('selectedTutorId')
        pair_id = data.get('selectedTuteeId')
        print(tutor_id)
        print(pair_id)

        if tutor_id is not None and pair_id is not None:
            # Create a new Pair instance and add it to the database
            pair = Pairs.query.get(pair_id)
            pair.tutor_id = tutor_id
            db.session.commit()

            # Query emails from the User table
            # Prepare a list containing both emails

            tutor = User.query.filter_by(id=tutor_id).all()
            tutee = User.query.filter_by(id=pair.tutee_id).all()
            print(tutor[0].email)
            print(tutee[0].email)

            u = Utils()
            u.send_mail(tutor[0].email,
                        'Branksome Hall Tutor Club',
                        'This email is to inform you that you are paired up with tutee: ' + tutee[0].first_name + ' ' + tutee[0].last_name + '. Please set up a time to begin!')
            u.send_mail(tutee[0].email,
                        'Branksome Hall Tutor Club',
                        'This email is to inform you that you are paired up with tutor: ' + tutor[0].first_name + ' ' + tutor[0].last_name + '. Please set up a time to begin!')

            db.session.close()

            flash("Students paired", category='success')
            return jsonify({"message": "Pair successfully added to the database"}), 200
        else:
            return jsonify({"error": "Invalid data"}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@auth.route('/hours', methods=['GET','POST'])
@login_required
def hours():
    return render_template("hours.html", user=current_user)