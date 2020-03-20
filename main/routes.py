from flask import render_template, Blueprint, redirect, url_for
from models import Content, Announcement

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('splash.html')

@main.route('/index')
def index():
    announcements = Announcement.query.all()
    first_page = Content.query.get(1)
    if first_page:
        return render_template('index.html', content=first_page.content, announcements = announcements)

    return redirect(url_for('main.home'))

@main.route('/faq')
def faq():
    return render_template('faq.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/announcements')
def announcements():
    announcements = Announcement.query.all()
    return render_template('announcements/index.html', data=announcements)


############# FOR TESTING SEARCHBAR #########
@main.route("/searchBarSample")
def searchBarSample():
    return render_template('searchBarSample.html')
#############################################
