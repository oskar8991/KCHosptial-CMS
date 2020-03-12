
from medications import medicationsList, generateChart
from flask import Flask, g, url_for, redirect, render_template, request, session, abort, flash, Response, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from functools import wraps
from sqlalchemy import *
from datetime import datetime


from flask_track_usage import TrackUsage
from flask_track_usage.storage.sql import SQLStorage
from flask_track_usage.storage.mongo import MongoEngineStorage
from flask_track_usage.summarization import sumRemote, sumUrl, sumUserAgent


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #configuring database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #causes significant overhead if True

# Tracks cookies - used for unique visitor count
app.config['TRACK_USAGE_COOKIE'] = True

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
class Content(db.Model):
    page_id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)


class flask_usage(db.Model):
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
    announcement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    #image = db.Column(db.BLOB)

db.create_all()


#
# TrackUsage Setup
#
pstore = SQLStorage(db=db)
t = TrackUsage(app, [pstore])


#Populate content table with input from add new page content
@app.route("/populateContent", methods=['POST'])
def populateContent():
    inputString = request.form['editBox']
    #INSERT INTO content (content) VALUES (inputString)
    newContent = Content(content = inputString)
    db.session.add(newContent)
    db.session.commit()
    return redirect(url_for('index'))

#Update content table with input from edit.html
@app.route("/updateContent", methods=['POST'])
def updateContent():
    inputString = request.form['editBox']
    conn = engine.connect()
    #UPDATE first row in table content
    updateStatement = f'UPDATE Content SET content="{inputString}" WHERE page_id=1'
    result = conn.execute(updateStatement)
    return redirect(url_for('index'))

@app.route('/index')
#content table query for index.html
def retrieveContentIndex():
    conn = engine.connect()
    select = "SELECT * FROM Content"
    result = conn.execute(select)
    outputRow = result.fetchone()
    for row in result:
        if (row.page_id == 1):
            outputRow = row
    return render_template('index.html', content=outputRow.content)

@app.route('/edit')
#content table query for Edit.html
def retrieveContentEdit():
    conn = engine.connect()
    select = "SELECT * FROM Content"
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

@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/about')
def about():
    return render_template('about.html')


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
    currentDate = datetime.today()
    currentMonth = currentDate.month
    currentDay = currentDate.day
    #Write handling of adding 0 when needed for the month
    yearDate = str(currentDate.year) + "-0" + str(currentMonth) + "-" + str(currentDay)
    yesterday = str(currentDate.year) + "-0" + str(currentMonth) + "-" + str(currentDay-1)

    #User Platform Usage Queries
    windowsCount = flask_usage.query.filter_by(ua_platform = 'windows').count()
    macCount = flask_usage.query.filter_by(ua_platform = 'macos').count()
    linuxCount = flask_usage.query.filter_by(ua_platform = 'linux').count()
    mobileCount = flask_usage.query.filter_by(ua_platform = 'mobile').count()

    #General Count Queries
    uniqueVisitorCount = db.session.query(flask_usage.remote_addr).distinct().count()
    mostVisitedPage = db.session.query(flask_usage.path, func.count(flask_usage.path).label('value_occurrence')).group_by(flask_usage.path).order_by(desc('value_occurrence')).first()
    totalVisits = db.session.query(flask_usage.id).count()

    #Visits for today ------

    visitsToday = db.session.query(flask_usage.id).filter(flask_usage.datetime>yearDate).count()

    # 1(day ago) - yesterday, 2 - 2 days ago, 3 - 3 days ago .. etc. up to 6 days ago - represents a week
    weekData = {'month' : str(currentMonth) , 'today' : {'date' : str(currentDay) +".0" + str(currentMonth), 'count' : visitsToday}}
    for i in range(1, 7):
        #Write handling of when months and years overlap NB!
        date = str((currentDay - i)) + ".0" + str(currentMonth)
        yearDate = str(currentDate.year) + "-0" + str(currentMonth) + "-" + str((currentDay-i))
        yearDate2 = str(currentDate.year) + "-0" + str(currentMonth) + "-" + str((currentDay-i+1))

        #Visits for the specified day
        weekData[f'{i}'] = {'date' : date , 'count' : db.session.query(flask_usage.id).filter(and_(flask_usage.datetime<yearDate2, flask_usage.datetime>yearDate)).count()}



    analyticsData = { 'weekData' : weekData , 'totalVisits' : totalVisits , 'mostVisitedPage' : mostVisitedPage , 'visitorCount' : uniqueVisitorCount , 'windowsCount' : windowsCount , 'macCount' : macCount , 'linuxCount' : linuxCount , 'mobileCount' : mobileCount}
    return render_template('dashboard.html', analyticsUsage=analyticsData)



@app.route("/edit")
@login_required
def edit():
    return render_template('edit.html')


@app.route("/users")
@login_required
def users():
    conn = engine.connect()
    query = "SELECT id, email from user"
    result = conn.execute(query)
    data = result.fetchall()
    return render_template('users.html', data = data)


@app.route("/addUser")
@login_required
def addUser():
    return render_template('addUser.html')

@app.route("/addContentUser", methods=['POST'])
def addContentUser():
    userEmail = request.form['userEmail']
    userPassword = request.form['userPassword']
    user = User(email = userEmail, password = userPassword)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users'))



@app.route('/announcements')
def announcements():
    return render_template('announcements.html')

@app.route('/addAnnouncementPage')
def addAnnouncementPage():
    return render_template('addAnnouncement.html')

@app.route('/editAnnouncementPage')
def editAnnouncementPage():
    id = request.args.get('id')
    title = request.args.get('title')
    description = request.args.get('description')
    return render_template('editAnnouncement.html', id=id, title=title, description=description)

@app.route('/deleteAnnouncementPage')
def deleteAnnouncementPage():
    id = request.args.get('id')
    title = request.args.get('title')
    description = request.args.get('description')
    return render_template('deleteAnnouncement.html', id=id, title=title, description=description)

@app.route('/editAnnouncement', methods=['POST'])
def editAnnouncement():
    id = request.form['announcementID']
    newTitle = request.form['newTitle']
    newDescription = request.form['newDescription']
    announcement = Announcement.query.filter_by(announcement_id = id).first()
    announcement.title = newTitle
    announcement.description = newDescription
    db.session.commit()
    conn = engine.connect()
    query = "SELECT * from announcement"
    result = conn.execute(query)
    data = result.fetchall()
    return render_template('announcements.html', data = data)

@app.route('/deleteAnnouncement', methods=['POST'])
def deleteAnnouncement():
    id = request.form['announcementID']
    announcement = db.session.query(Announcement).filter(Announcement.announcement_id == id).first()
    db.session.delete(announcement)
    db.session.commit()
    conn = engine.connect()
    query = "SELECT * from announcement"
    result = conn.execute(query)
    data = result.fetchall()
    return render_template('announcements.html', data = data)

@app.route("/addAnnouncement", methods=['POST'])
@login_required
def addAnnouncement():
    title = request.form['title']
    description = request.form['description']
    date = datetime.now()
    #image = request.files['imageUpload']
    announcement = Announcement(title = title, description = description, date = date)
    db.session.add(announcement)
    db.session.commit()
    conn = engine.connect()
    query = "SELECT * from announcement"
    result = conn.execute(query)
    data = result.fetchall()
    return render_template('announcements.html', data = data)

@app.route("/showAnnouncements", methods=['GET'])
def showAnnouncements():
    conn = engine.connect()
    query = "SELECT * from announcement"
    result = conn.execute(query)
    data = result.fetchall()
    #images = [(base64.b64encode(item['image'] for item in result.fetchall()).DATA).encode('ascii')]
    #imagesRaw = [item['image'] for item in result.fetchall()]
    #imagesFormatted = []
    #for x in imagesRaw:
    #    imagesFormatted.append(base64.b64encode(x.DATA))
    return render_template('announcements.html', data = data)



############# FOR TESTING SEARCHBAR #########
@app.route("/searchBarSample")
def searchBarSample():
    return render_template('searchBarSample.html')
#############################################




if __name__ == '__main__':
    app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
