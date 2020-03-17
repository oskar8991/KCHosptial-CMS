from flask import (Blueprint, request, render_template, session, redirect, 
                   url_for, flash)
from flask_login import login_required
from app import db, bcrypt
from models import User

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email = request.form['username']).first()

        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            session['logged_in'] = True
            return redirect(url_for('dashboard.dashboard_panel'))
        else:
            flash('Invalid credentials')

    return render_template('auth/login.html')

@login_required
@users.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('main.index'))

@login_required
@users.route("/users")
def list_users():
    return render_template('users.html', data = User.query.all())

@login_required
@users.route("/users/add", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['userPassword']).decode('utf-8')
        user = User(
            email = request.form['userEmail'], 
            password = hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.list_users'))

    return render_template('add_user.html')

@login_required
@users.route("/users/delete/<user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('list_users'))