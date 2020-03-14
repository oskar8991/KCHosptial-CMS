from flask import (Blueprint, request, render_template, session, redirect, 
                   url_for, flash)
from models import User
from flask_login import login_required

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email = request.form['username']).first()

        if not user or user.password != request.form['password']:
            flash('Invalid credentials')
        else:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))

    return render_template('auth/login.html')

@login_required
@users.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('main.index'))