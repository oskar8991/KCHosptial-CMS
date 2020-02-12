from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #configuring database
db = SQLAlchemy(app) 


#Creates a table for login form with id, email and password 
class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(20), nullable=False)
	password = db.Column(db.String(20), nullable=False)


#returning self id
#def __repr__(self):
#	return '<Task %r>' % self.id


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['password'] != 'admin':
            flash('Invalid credentials')
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('auth/login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()



if __name__ == '__main__':
    app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
