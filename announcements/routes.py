from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required
from datetime import datetime
from app import db
from models import Announcement

announcements = Blueprint('announcements', __name__)

@login_required
@announcements.route('/announcements/create', methods=['GET', 'POST'])
def create_announcement():
    if request.method == 'POST':
        announcement = Announcement(
            title = request.form['title'], 
            description = request.form['description'], 
            date = datetime.now()
        )
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for('main.announcements'))

    return render_template('announcements/create.html')

@login_required
@announcements.route('/announcements/edit', methods=['GET', 'POST'])
def edit_announcement():
    if request.method == 'POST':
        announcement = Announcement.query.get(int(request.form['announcementID']))

        if announcement:
            announcement.title = request.form['newTitle']
            announcement.description = request.form['newDescription']
            db.session.commit()
        
        return redirect(url_for('main.announcements'))

    return render_template('announcements/edit.html',
        id = request.args.get('id'),
        title = request.args.get('title'),
        description = request.args.get('description')
    )

@login_required
@announcements.route('/announcements/delete', methods=['GET', 'POST'])
def delete_announcement():
    if request.method == 'POST':
        announcement = Announcement.query.get(int(request.form['announcementID']))
        if announcement:
            db.session.delete(announcement)
            db.session.commit()
        
        return redirect(url_for('main.announcements'))

    return render_template('announcements/delete.html',
        id = request.args.get('id'),
        title = request.args.get('title'),
        description = request.args.get('description')
    )
