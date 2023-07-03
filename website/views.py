from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) # homepage
@login_required
def home():
    if request.method == 'GET':
        return render_template("home.html", user=current_user)

@views.route('/user', methods=['GET', 'POST']) # user page
@login_required
def user():
    users = User.query.all()
    print(users)
    if request.method == 'GET':
        print("Get request on user page.")
        print(len(users))
        return render_template("user.html", user=current_user, users=users)

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