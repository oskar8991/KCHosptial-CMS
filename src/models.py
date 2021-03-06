from flask_login import UserMixin
from app import login_manager, db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Creates a table for login form with id, email and password
class User(UserMixin, db.Model):
    __tablename__ = 'app_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

#Creates a table for web page content with id and text
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    title = db.Column(db.Text, nullable=True)
    question = db.relationship("Questions", backref='content', cascade="delete")

class FlaskUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    url = db.Column(db.String(128))
    ua_browser = db.Column(db.String(16))
    ua_language = db.Column(db.String(16))
    ua_platform = db.Column(db.String(16))
    ua_version = db.Column(db.String(16))
    blueprint = db.Column(db.String(16))
    view_args = db.Column(db.String(64))
    status = db.Column(db.Integer)
    remote_addr = db.Column(db.String(24))
    xforwardedfor = db.Column(db.String(24))
    authorization = db.Column(db.Boolean)
    ip_info = db.Column(db.String(1024))
    path = db.Column(db.String(128))
    speed = db.Column(db.Float)
    datetime = db.Column(db.DateTime)
    username = db.Column(db.String(128))
    track_var = db.Column(db.String(128))

#Creates a table to store announcements with id, title, date, description
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    links = db.Column(db.String(300), nullable=True, default="N/A")
    #image = db.Column(db.BLOB)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(128), nullable=False)
    answer = db.relationship("Answers", backref='question', cascade="delete")
    content_id = db.Column(db.Integer(), db.ForeignKey('content.id'), nullable=False)
    stat_right = db.Column(db.Integer(), default=0)
    stat_wrong = db.Column(db.Integer(), default=0)

class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_text = db.Column(db.String(64), nullable=False)
    correct = db.Column(db.Integer(), unique=False, nullable=False)
    question_id = db.Column(db.Integer(), db.ForeignKey('questions.id'), nullable=False)

#Creates a table to store FAQ Question and answer
class FAQQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(400), nullable=False)
    answer = db.Column(db.String(10000), nullable=False)

# Creates table for about page cards
class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), nullable=False)
    content = db.Column(db.String(10000), nullable=False)

class Glossary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.Text)
    description = db.Column(db.Text)

class Helpful(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(400), nullable=False)
    yes = db.Column(db.Integer(), default=0)
    no = db.Column(db.Integer(), default=0)

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), nullable=False)
    given_hours = db.Column(db.Integer(), nullable=False)
    indications = db.Column(db.String(400), default='N/A')


def init_db():
    db.create_all()
