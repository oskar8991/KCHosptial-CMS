from flask import (Blueprint, request, render_template, session, redirect, 
                   url_for, flash)
from flask_login import login_required
from models import User
from app import db

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email = request.form['username']).first()

        if not user or user.password != request.form['password']:
            flash('Invalid credentials')
        else:
            session['logged_in'] = True
            return redirect(url_for('dashboard.dashboard_panel'))

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
        user = User(
            email = request.form['userEmail'], 
            password = request.form['userPassword']
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.list_users'))

    return render_template('add_user.html')