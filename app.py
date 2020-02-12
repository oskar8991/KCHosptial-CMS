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


if __name__ == '__main__':
    app.run(debug=True)
