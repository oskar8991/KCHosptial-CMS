from flask import (Blueprint, request, render_template, session, redirect, 
                   url_for, flash)
from flask_login import login_required, login_user, logout_user, current_user
from app import db, bcrypt
from models import User
from users.forms import LoginForm, AddUserForm

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_panel'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard.dashboard_panel'))
        else:
            flash('Invalid credentials.', 'warning')

    return render_template('users/login.html', form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route("/users")
@login_required
def list_users():
    return render_template('users/list_users.html', data = User.query.all())

@users.route("/users/add", methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('User account has been created.', 'success')
        return redirect(url_for('users.list_users'))

    return render_template('users/add_user.html', form=form)

@users.route("/users/delete/<user_id>")
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('users.list_users'))