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
        # subject4 = request.form.get('subject4')
        # subject5 = request.form.get('subject5')
        teacher_email = request.form.get('teacher_email')
        parent_email = request.form.get('parent_email')
        print(request.form.get("is_boarding"))
        is_boarding = request.form.get('is_boarding')
        user = User.query.filter_by(email=email).first()
        subjects_list = []

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
        elif email == parent_email:
            flash('The email of your parent cannot be your email.', category='error')
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
                subject4="",
                subject5="",
                pair_num=0,
                is_boarding=is_boarding
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            new_pairs = Pairs(tutee_id=current_user.id,tutor_id=0, subject=subject1)
            db.session.add(new_pairs)
            db.session.commit()

            subjects_list.append(subject1)

            if len(subject2) > 0:
                new_pairs = Pairs(tutee_id=current_user.id, tutor_id=0,subject=subject2)
                db.session.add(new_pairs)
                db.session.commit()
                subjects_list.append(subject2)

            if len(subject3) > 0:
                new_pairs = Pairs(tutee_id=current_user.id, tutor_id=0, subject=subject3)
                db.session.add(new_pairs)
                db.session.commit()
                subjects_list.append(subject3)

            # if len(subject4) > 0:
            #     new_pairs = Pairs(tutee_id=current_user.id, tutor_id=0, subject=subject4)
            #     db.session.add(new_pairs)
            #     db.session.commit()
            #     subjects_list.append(subject4)
            #
            # if len(subject5) > 0:
            #     new_pairs = Pairs(tutee_id=current_user.id, tutor_id=0, subject=subject5)
            #     db.session.add(new_pairs)
            #     db.session.commit()
            #     subjects_list.append(subject5)

            u = Utils()
            u.send_mail(parent_email,
                        'Confirmation of Enrollment of ' + first_name + ' ' + last_name + ' in the Branksome Hall Tutor Program',
                        'Hello!' 
                        '\n\nThis email is to inform you that your child, ' + first_name + ' ' + last_name + ', is signed up as a tutee for the Branksome Hall Tutor Program for: ' + ', '.join(subjects_list) + '.'
                        '\n\nThe peer tutoring program is designed to provide additional support and guidance in these subjects. A tutor will be assigned soon, and you will get more details about the pairing. If you have any questions or need any help, please do not hesitate to contact Ms. Contreras at mcontreras@branksome.on.ca or Ms. Blyth at cblyth@branksome.on.ca.'
                        '\n\nThank you for your support, and we look forward to a successful tutoring experience!'
                        '\n\nSincerely, '
                        '\n\nThe Peer Tutoring Team')
            u.send_mail(email,
                        'Welcome to the Branksome Hall Tutor Program!',
                        'Dear ' + first_name + ' ' + last_name + ','
                        '\n\nThank you for signing up for the Branksome Hall Tutor Program! We are excited to help you excel in the following subjects: ' + ', '.join(subjects_list) + '!'
                        '\n\nYou will soon be paired with a tutor who will assist you in these areas. Please keep an eye on your email for further instructions regarding your tutor assignment.'
                        '\n\nIf you have any questions or need additional information, feel free to reach out to Ms. Contreras at mcontreras@branksome.on.ca or Ms. Blyth at cblyth@branksome.on.ca. You can also reach Vita Huang at vhuang@branksome.on.ca and Megan Kwan at mkwan@branksome.on.ca who are the 2024-2025 club heads.'
                        '\n\nWe wish you a productive and enriching experience in the program!'
                        '\n\nSincerely,'
                        '\n\nThe Peer Tutoring Team'
                        )

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
        is_boarding = request.form.get('is_boarding')
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
        elif email == parent_email:
            flash('The email of your parent cannot be your email.', category='error')
        else:
            new_user = User(email=email,
                            first_name=first_name,
                            last_name=last_name,
                            password=generate_password_hash(password1,method='sha256'),
                            role=role,
                            grade=grade,
                            parent_email=parent_email,
                            subject1=subject,
                            teacher_email=teacher_email,
                            pair_num=0,
                            is_boarding= is_boarding)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            u = Utils()
            u.send_mail(parent_email,
                        'Confirmation of Enrollment of ' + first_name + ' ' + last_name + ' in the Branksome Hall Tutor Program',
                        'Hello!'
                        '\n\nThis email is to inform you that your child, ' + first_name + ' ' + last_name + ', is signed up as a tutor for the Branksome Hall Tutor Program for ' + subject + '.'
                        '\n\nThe program is committed to providing excellent support to students, and ' + first_name + ' will play a crucial role in this effort.'
                        '\n\nIf you have any questions, please directly contact Ms. Contreras or Ms. Blyth. Thank you for your support, and we look forward to a successful tutoring experience!'
                        '\n\nSincerely,'
                        '\n\nThe Peer Tutoring Team')
            u.send_mail(email,
                        'Welcome to the Branksome Hall Tutor Program!',
                        'Dear ' + first_name + ','
                        '\n\nThank you for joining the Branksome Hall Tutor Program as a tutor! We are thrilled to have you on board and are confident that your expertise in ' + subject + ' will greatly benefit our students.'
                        '\n\nYou will soon receive further details about your assigned tutees and the next steps in the program. Please keep an eye on your email for updates and instructions!'
                        '\n\nIf you have any questions or require additional information, please feel free to reach out to Ms. Contreras at mcontreras@branksome.on.ca or Ms. Blyth at cblyth@branksome.on.ca. You can also email the 2024-2025 club heads: Vita Huang (vhuang@branksome.on.ca) and Megan Kwan (mkwan@branksome.on.ca).'
                        '\n\nWe look forward to working with you and achieving great results together!'
                        '\n\nSincerely,'
                        '\n\nThe Peer Tutoring Team')

            flash('Account created!', category='success')
            print("account created")
            return redirect(url_for('auth.hours'))

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

            tutor = User.query.filter_by(id=tutor_id).first()
            tutee = User.query.filter_by(id=pair.tutee_id).first()
            tutor.pair_num =  tutor.pair_num +1
            db.session.commit()
            print(tutor.email)
            subject=""
            if tutor.subject1 is not None and len(tutor.subject1)>0:
                subject+=tutor.subject1 + ","

            if tutor.subject2 is not None and len(tutor.subject2)>0:
                subject += tutor.subject2 + ","

            print(tutee.email)

            tutee_subject=""
            if tutee.subject1 is not None and len(tutee.subject1)>0:
                tutee_subject += tutee.subject1 + ","

            if tutee.subject2 is not None and len(tutee.subject2)>0:
                tutee_subject += tutee.subject2 + ","

            if tutee.subject3 is not None and len(tutee.subject3)>0:
                tutee_subject += tutee.subject3 + ","

            # if tutee.subject4 is not None and len(tutee.subject4)>0:
            #     tutee_subject += tutee.subject4 + ","
            #
            # if tutee.subject5 is not None and len(tutee.subject5)>0:
            #     tutee_subject += tutee.subject5 + ","

            u = Utils()
            u.send_mail(tutor.email,
                        'You Have Been Paired with a Tutee!',
                        'Dear ' + tutor.first_name + ','
                        '\n\nWe are pleased to inform you that you have been paired with a tutee: ' + tutee.first_name + ' ' + tutee.last_name + ' for ' + tutor.tutor_subject + '. '
                        '\n\nPlease reach out to ' + tutee.first_name + ' to schedule your first meeting and begin the tutoring sessions. We trust that your expertise will be incredibly beneficial to their learning experience. We recommend first emailing them and establishing a point of connection, whether that be through text, email, or other social media platforms. That way, it will be easier to get updates on your sessions and schedule regular ones.'
                        '\n\nAs a reminder, please upload your hours to the "Time Entry" page on the website promptly if you wish to get service hours.'
                        '\n\nIf you have any questions or need assistance, please contact Ms. Contreras at mcontreras@branksome.on.ca or Ms. Blyth at cblyth@branksome.on.ca. You can also direct your questions to the 2024-2025 club heads: Vita Huang (vhuang@branksome.on.ca) and Megan Kwan (mkwan@branksome.on.ca). Thank you for your dedication to our program!'
                        '\n\nSincerely,'
                        '\n\nThe Peer Tutoring Team')
            u.send_mail(tutee.email,
                        'You Have Been Paired with a Tutor!',
                        'Dear ' + tutee.first_name + ','
                        '\n\nWe are excited to inform you that you have been paired with a tutor, ' + tutor.first_name + ' ' + tutor.last_name + ', for ' + subject + '. '
                        '\n\n' + tutor.first_name + ' will reach out shortly to schedule your first meeting and start your tutoring sessions. We believe this pairing will greatly enhance your learning experience in these subjects.'
                        '\n\n If your tutor does not reach out promptly, you can try emailing them as well. If you have any questions, feel free to contact Ms. Contreras at mcontreras@branksome.on.ca, Ms. Blyth at cblyth@branksome.on.ca, Vita Huang at vhuang@branksome.on.ca or Megan Kwan at mkwan@branksome.on.ca. Ms. Contreras and Ms. Blyth are the teachers responsible for the programs and Vita and Megan are the 2024-2025 club heads.'
                        '\n\nWe hope that you have a productive year and feel more confident in ' + subject + '!'
                        '\n\nSincerely,'
                        '\n\nThe Peer Tutoring Team')

            db.session.close()

            flash("Students successfully paired!", category='success')
            return jsonify({"success": True,"message": "Pair successfully added to the database"}), 200
        else:
            return jsonify({"success": False,"error": "Invalid data"}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@auth.route('/hours', methods=['GET','POST'])
@login_required
def hours():
    return render_template("hours.html", user=current_user)