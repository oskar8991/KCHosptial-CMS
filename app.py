from flask import Flask
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

#Populate content table with input from add new page content
@app.route("/populateContent", methods=['POST'])
def populateContent():
    inputString = request.form['editBox']
    #INSERT INTO content (content) VALUES (inputString)
    insertStatement = pageContent.insert().values(content = inputString)
    conn = engine.connect()
    result = conn.execute(insertStatement)
    return redirect(url_for('index'))

#Update content table with input from edit.html
@app.route("/updateContent", methods=['POST'])
def updateContent():
    inputString = request.form['editBox']
    #UPDATE first row in table content
    updateStatement = pageContent.update().where(pageContent.c.page_id==1).values(content = inputString)
    conn = engine.connect()
    result = conn.execute(updateStatement)
    return redirect(url_for('index'))


@app.route('/index')
#content table query for index.html
def retrieveContentIndex():
    # Equivalent to SELECT * FROM pageContent
    select = pageContent.select()
    conn = engine.connect()
    result = conn.execute(select)
    outputRow = result.fetchone()
    for row in result:
        if (row.page_id == 1):
            outputRow = row
    return render_template('index.html', content=outputRow.content)

@app.route('/edit')
#content table query for Edit.html
def retrieveContentEdit():
    # Equivalent to SELECT * FROM pageContent
    select = pageContent.select()
    conn = engine.connect()
    result = conn.execute(select)
    outputRow = result.fetchone()
    for row in result:
        if (row.page_id == 1):
            outputRow = row
    return render_template('edit.html', content=outputRow.content)




@app.route('/medication', methods=['GET', 'POST'])
def medication():
    if request.method == 'POST':
        selected = [med for med in medicationsList if med.name in request.form]
        return render_template('chart.html', chart=generateChart(selected))

    return render_template('medication.html', medications=medicationsList)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


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

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import create_engine, MetaData


from flask_track_usage import TrackUsage
from flask_track_usage.storage.sql import SQLStorage

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuring database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    # Causes significant overhead if True.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Tracks cookies - used for unique visitor count
    app.config['TRACK_USAGE_COOKIE'] = True

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'


    from models import User, init_db
    with app.app_context():
        init_db()
        # TrackUsage Setup
        pstore = SQLStorage(db=db)
        t = TrackUsage(app, [pstore])

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from drug_chart.routes import drug_chart
    from users.routes import users
    from main.routes import main
    from announcements.routes import announcements
    from faq.routes import faq
    from content.routes import content
    from dashboard.routes import dashboard
    from quiz.routes import quiz

    blueprints = [drug_chart, users, main, announcements, faq, content, dashboard, 
        quiz
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        t.include_blueprint(blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
