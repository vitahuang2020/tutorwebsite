from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from.import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # print(user.first_name)
                flash(user.first_name + ' is logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html",user=current_user)
# hello

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')
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
        else:
            # add user to database

            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1,method='sha256'), role=role, subjects="")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash ('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/request-role', methods = ['GET', 'POST'])
def request_role():
    if request.method == 'POST':
        math = request.form.get('math')
        english = request.form.get('english')
        geography = request.form.get('geography')
        history = request.form.get('history')
        physics = request.form.get('physics')
        chemistry = request.form.get('chemistry')
        biology = request.form.get('biology')
        french = request.form.get('french')
        mandarin = request.form.get('mandarin')
        compsci = request.form.get('compsci')

        subjects = ""
        if math == "math":
            subjects += "math "
        if english == "english":
            subjects += "english "
        if geography == "geography":
            subjects += "geography "
        if history == "history":
            subjects += "history "
        if physics == "physics":
            subjects += "physics "
        if chemistry == "chemistry":
            subjects += "chemistry "
        if biology == "biology":
            subjects += "biology "
        if french == "french":
            subjects += "french "
        if mandarin == "mandarin":
            subjects += "mandarin "
        if compsci == "compsci":
            subjects += "compsci "

        print(subjects)

        timeAvailable = ""

        weekday = ["mon", "tue", "wed", "thur", "fri"]
        for day in weekday:
            morning = request.form.get(day + 'Morning')
            lunch = request.form.get(day + 'Lunch')
            afternoon = request.form.get(day + 'Afternoon')

            if morning == day + 'Morning':
                timeAvailable += day + 'Morning '
            if lunch == day + 'Lunch':
                timeAvailable += day + 'Lunch '
            if afternoon == day + 'Afternoon ':
                timeAvailable += day + 'Afternoon '

        print(timeAvailable)

        User.verified = True
        User.subjects = subjects
        User.timeAvailable = timeAvailable
        db.session.commit()

        return redirect(url_for('views.home'))

    return render_template("request_role.html", user=current_user)