from flask import Flask, url_for, redirect, render_template, request, session, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #configuring database
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


#Creates a table for login form with id, email and password
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(20), nullable=False)
	password = db.Column(db.String(20), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route("/logmein", methods=['POST'])
def logmein():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(email = username).first()

    if user.password != password:
        flash('Invalid credentials')
        return render_template('auth/login.html') 
    else:
        session['logged_in'] = True
        return redirect(url_for('index'))



@app.route("/logout")
@login_required
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
