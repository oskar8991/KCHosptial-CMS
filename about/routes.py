from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required
from app import db
from models import About

about = Blueprint('about', __name__)

@about.route('/about/create', methods=['GET', 'POST'])
@login_required
def create_card():
    if request.method == 'POST':
        about = About(
            title = request.form['title'],
            content = request.form['content'], 
        )
        db.session.add(about)
        db.session.commit()
        return redirect(url_for('main.about'))

    return render_template('about/create.html')

@about.route('/about/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_card(id):
    about = About.query.get(id)
    if request.method == 'POST':
        if about:
            about.question = request.form['newTitle']
            about.content = request.form['newContent']
            db.session.commit()
        
        return redirect(url_for('main.about'))

    return render_template('about/edit.html', about=about)

@about.route('/about/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_card(id):
    about = About.query.get(id)
    if request.method == 'POST':
        if about:
            db.session.delete(about)
            db.session.commit()
        
        return redirect(url_for('main.about'))

    return render_template('about/delete.html', about=about)
