from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note, User, Pairs
from . import db
import json
from sqlalchemy.orm import aliased

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST']) # homepage
@login_required
def home():
    tutors = User.query.filter_by(role='tutor').all()
    tutees = User.query.filter_by(role='tutee').all()
    # pairs = Pairs.query.all()

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
        UserTutee.first_name.label("tutee_first_name"),
        UserTutee.last_name.label("tutee_last_name")
    ).all())

    print(pairs_list)

    print(tutors)
    if request.method == 'GET':
        print("Get request on home page.")
        print(len(tutors))
        return render_template("home.html", user=current_user, tutors=tutors, tutees=tutees, pairs_list=pairs_list)

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
#
#     return jsonify({})
