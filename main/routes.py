from flask import render_template, Blueprint, redirect, url_for
from models import Content, Announcement, FAQQuestions, About

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('splash.html')

@main.route('/index')
def index():
    #first_page = Content.query.get(1)
    return render_template('index.html')#, content=first_page.content)


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


############# FOR TESTING SEARCHBAR #########
@main.route("/searchBarSample")
def searchBarSample():
    return render_template('searchBarSample.html')
#############################################
