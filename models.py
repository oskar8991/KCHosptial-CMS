from dataclasses import dataclass
from typing import List
from flask_login import UserMixin
from app import login_manager, db

@dataclass
class Medication:
    name: str
    time: List[int]
    indications: int = 'N/A'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Creates a table for login form with id, email and password
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

#Creates a table for web page content with id and text
class Content(db.Model):
    page_id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    title = db.Column(db.Text, nullable=True)


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
    path = db.Column(db.String(32))
    speed = db.Column(db.Float)
    datetime = db.Column(db.DateTime)
    username = db.Column(db.String(128))
    track_var = db.Column(db.String(128))

#Creates a table to store announcements with id, title, date, description
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    #image = db.Column(db.BLOB)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(30), nullable=False)
    answer = db.relationship("Answers", backref='question', cascade="delete")

class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_text = db.Column(db.String(30), nullable=False)
    correct = db.Column(db.Integer(), unique=False, nullable=False)
    question_id = db.Column(db.Integer(), db.ForeignKey('questions.id'), nullable=False)

#Creates a table to store FAQ Question and answer
class FAQQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(400), nullable=False)
    answer = db.Column(db.String(10000), nullable=False)

# Creates table for about page cards
class About(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(400), nullable=False)
    content = db.Column(db.String(10000), nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    page_ref = db.Column(db.Integer(), db.ForeignKey('content.page_id'), nullable=False)

class Glossary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.Text)
    description = db.Column(db.Text)
#NEed to create a table like answers that connects the questions to the a specific quiz

def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()
