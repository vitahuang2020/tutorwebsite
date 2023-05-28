from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) # homepage
@login_required
def home():
    users = User.query.all()
    if request.method == 'GET':
        print("Get request on home page.")
        print(len(users))
        return render_template("home.html", user=current_user, users=users)

    elif request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

        return render_template("home.html", user=current_user, users=users)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

#hello j