from flask import render_template, Blueprint, redirect, url_for, request, jsonify
from models import Content, Announcement, FAQQuestions, About, Glossary, Helpful
from content.utils import *

#from app import mail
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('splash.html')

@main.route('/index')
def index():
    announcements = Announcement.query.all()
    contentDictionary = {
        'headings' : get_headings(),
        'records' : get_records(),
        'glossary' : get_glossary(),
        'questions': assossiated_questions()
    }

    return render_template('index.html', content=contentDictionary, announcements=announcements)

@main.route('/faq')
def faq():
    faqs = FAQQuestions.query.all()
    return render_template('faq/index.html', data=faqs)

@main.route('/about')
def about():
    about = About.query.all()
    return render_template('about/index.html', data=about)

@main.route('/announcements')
def announcements():
    announcements = Announcement.query.all()
    return render_template('announcements/index.html', data=announcements)


@main.route("/something-wrong", methods=['GET', 'POST'])
def somethingWrong():
    if request.method == 'POST':
        problem = request.form.get('problem')
        msg = Message(problem, recipients=["to@example.com"])
        #mail.send(msg) once we deploy we can configure the server
        return render_template('feedback.html')

    return render_template('somethingWrong.html')



############# FOR TESTING SEARCHBAR #########
@main.route("/searchBarSample")
def searchBarSample():
    return render_template('searchBarSample.html')
#############################################

@main.route('/_helpful_feedback')
def helpful_feedback():
    page = request.args.get('page', '', type=str)
    answer = request.args.get('answer', -1, type=int)

    if page == '' or answer == -1:
        return jsonify(result="An error occured.")

    helpful = Helpful.query.filter_by(page = page).first()
    create = (helpful is None)
    if create:
        helpful = Helpful(page=page, yes=0, no=0)

    if answer:
        helpful.yes = helpful.yes + 1
    else:
        helpful.no = helpful.no + 1

    if create:
        db.session.add(helpful)
    db.session.commit()

    return jsonify(result="Thank You for your feedback!")
