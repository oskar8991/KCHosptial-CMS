from flask import Flask, url_for, redirect, render_template, request, session, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from functools import wraps
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #configuring database
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

engine = create_engine('sqlite:///data.db', echo = True)
meta = MetaData()


#Creates a table for login form with id, email and password
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

#Creates a table for web page content with id and text
pageContent = Table(
    'content', meta,
    Column("page_id", Integer, primary_key=True),
    Column("content", Text),
)
meta.create_all(engine)

'''
class Page(Base):
    __tablename__ = 'content'
    Column("page_id", Integer, primary_key=True)
    Column("content", Text)
'''

#Populate content table with input from edit.html
#INSERT INTO content (content) VALUES (inputString)
@app.route("/populateContent", methods=['POST'])
def populateContent():
    inputString = request.form['editBox']
    insertStatement = pageContent.insert().values(content = inputString)
    conn = engine.connect()
    result = conn.execute(insertStatement)
    return redirect(url_for('index'))


#content table query
def retrieveContent():
    # Equivalent to SELECT * FROM pageContent
    select = pageContent.select()
    conn = engine.connect()
    result = conn.execute(select)
    row = result.fetchone()
    for row in result:
        print(row.content)
        return "<p>" + row.content + "<p>"


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

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap    

@app.route("/logmein", methods=['POST'])
def logmein():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(email = username).first()

    if not user:
        flash('Invalid credentials')
        return redirect(url_for('login'))
    else:
        if user.password != password:
            flash('Invalid credentials')
            return redirect(url_for('login'))
        else:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))



@app.route("/logout")
@login_required
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('index'))
    

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/edit")
@login_required
def edit():
    return render_template('edit.html')
            


if __name__ == '__main__':
    app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
