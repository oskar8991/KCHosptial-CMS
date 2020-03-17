from flask import (Blueprint, request, render_template, session, redirect, 
                   url_for, flash)
from flask_login import login_required
from app import db, bcrypt
from models import User
from users.forms import LoginForm, AddUserForm

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['logged_in'] = True
            return redirect(url_for('dashboard.dashboard_panel'))
        else:
            flash('Invalid credentials.', 'warning')

    return render_template('auth/login.html', form=form)

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
    form = AddUserForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('User account has been created.', 'success')
        return redirect(url_for('users.list_users'))

    return render_template('add_user.html', form=form)

@login_required
@users.route("/users/delete/<user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('users.list_users'))