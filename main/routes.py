from flask import render_template, Blueprint
from models import Content, Announcement

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('index.html')

@main.route('/index')
def index():
    first_page = Content.query.get(1)
    return render_template('index.html', content=first_page.content)

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