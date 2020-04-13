from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required
from datetime import datetime
from app import db
from models import Announcement

announcements = Blueprint('announcements', __name__)

@announcements.route('/announcements/create', methods=['GET', 'POST'])
@login_required
def create_announcement():
    if request.method == 'POST':
        announcement = Announcement(
            title = request.form['title'], 
            description = request.form['description'], 
            date = datetime.now(),
            links = request.form['links']
        )
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for('main.announcements'))

    return render_template('announcements/create.html')

@announcements.route('/announcements/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    announcement = Announcement.query.get(id)
    if request.method == 'POST':
        if announcement:
            announcement.title = request.form['newTitle']
            announcement.description = request.form['newDescription']
            announcement.links = request.form['newLinks']
            db.session.commit()
        
        return redirect(url_for('main.announcements'))

    return render_template('announcements/edit.html', announcement=announcement)

@announcements.route('/announcements/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_announcement(id):
    announcement = Announcement.query.get(id)
    if request.method == 'POST':
        if announcement:
            db.session.delete(announcement)
            db.session.commit()
        
        return redirect(url_for('main.announcements'))

    return render_template('announcements/delete.html', announcement=announcement)
