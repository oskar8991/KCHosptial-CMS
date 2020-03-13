
from medications import medicationsList, generateChart
from flask import Flask, g, url_for, redirect, render_template, request, \
    session, abort, flash, Response, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from sqlalchemy import *
from datetime import datetime, timedelta


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


# TrackUsage Setup
pstore = SQLStorage(db=db)
t = TrackUsage(app, [pstore])


def db_execute(query):
    conn = engine.connect()
    return conn.execute(query)

#Populate content table with input from add new page content
@app.route("/populateContent", methods=['POST'])
def populateContent():
    #INSERT INTO content (content) VALUES (inputString)
    db.session.add(Content(content = request.form['editBox']))
    db.session.commit()
    return redirect(url_for('index'))

#Update content table with input from edit.html
@app.route("/updateContent", methods=['POST'])
def updateContent():
    #UPDATE first row in table content
    db_execute(
        f'UPDATE Content SET content="{request.form["editBox"]}" WHERE page_id=1'
    )
    
    return redirect(url_for('index'))

@app.route('/index')
#content table query for index.html
def retrieveContentIndex():
    query = "SELECT * FROM Content"
    result = db_execute(query)
    outputRow = result.fetchone()

    for row in result:
        if (row.page_id == 1):
            outputRow = row

    return render_template('index.html', content=outputRow.content)

@app.route('/edit')
#content table query for Edit.html
def retrieveContentEdit():
    query = "SELECT * FROM Content"
    result = db_execute(query)
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
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap

@app.route("/logmein", methods=['POST'])
def logmein():
    user = User.query.filter_by(email = request.form['username']).first()

    if not user or user.password != request.form['password']:
        flash('Invalid credentials')
        return redirect(url_for('login'))
    else:
        session['logged_in'] = True
        return redirect(url_for('dashboard'))



@login_required
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('index'))


@login_required
@app.route("/dashboard")
def dashboard():
    today = datetime.today()

    visitsToday = db.session.query(flask_usage.id).filter(
        flask_usage.datetime > func.DATE(today)
    ).count()

    weekData = {
        'month': today.strftime("%m"),
        'today': {
            'date': today.strftime("%d/%m"),
            'count': visitsToday
        }
    }
    
    # 1(day ago) - yesterday, 2 - 2 days ago, 3 - 3 days ago .. etc. up to 6 days ago - represents a week
    for i in range(1, 7):
        day = datetime.today() - timedelta(days=i)

        count = db.session.query(flask_usage.id).filter(and_(
            flask_usage.datetime < func.DATE(day + timedelta(days=1)),
            flask_usage.datetime > func.DATE(day)
        )).count()

        #Visits for the specified day
        weekData[str(i)] = {'date' : day.strftime("%d/%m") , 'count' : count}


    analyticsData = {
        'weekData': weekData,
        
        #User Platform Usage Queries
        'windowsCount': (flask_usage.query
                                    .filter_by(ua_platform = 'windows')
                                    .count()),
        'macCount': (flask_usage.query
                                .filter_by(ua_platform = 'macosx')
                                .count()),
        'linuxCount': (flask_usage.query
                                  .filter_by(ua_platform = 'linux')
                                  .count()),
        'mobileCount': (flask_usage.query
                                   .filter_by(ua_platform = 'mobile')
                                   .count()),

        #General Count Queries
        'visitorCount': (db.session.query(flask_usage.remote_addr)
                                   .distinct()
                                   .count()),
        'mostVisitedPage': (db.session.query(
                flask_usage.path,
                func.count(flask_usage.path).label('value_occurrence')
            ).group_by(flask_usage.path)
            .order_by(desc('value_occurrence'))
            .first()),
    
        'totalVisits': db.session.query(flask_usage.id).count()
    }

    return render_template('dashboard.html', analyticsUsage=analyticsData)


@login_required
@app.route("/edit")
def edit():
    return render_template('edit.html')

@login_required
@app.route("/users")
def users():
    query = "SELECT id, email from user"
    return render_template('users.html', data = db_execute(query).fetchall())

@login_required
@app.route("/addUser")
def addUser():
    return render_template('addUser.html')

@app.route("/addContentUser", methods=['POST'])
def addContentUser():
    user = User(
        email = request.form['userEmail'], 
        password = request.form['userPassword']
    )
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
    return render_template('editAnnouncement.html',
        id = request.args.get('id'),
        title = request.args.get('description'),
        description = request.args.get('description')
    )

@app.route('/deleteAnnouncementPage')
def deleteAnnouncementPage():
    return render_template('deleteAnnouncement.html',
        id = request.args.get('id'),
        title = request.args.get('title'),
        description = request.args.get('description')
    )

@app.route('/editAnnouncement', methods=['POST'])
def editAnnouncement():
    announcement = Announcement.query.filter_by(
        announcement_id = request.form['announcementID']
    ).first()

    announcement.title = request.form['newTitle']
    announcement.description = request.form['newDescription']
    db.session.commit()
    
    query = "SELECT * from announcement"
    return render_template('announcements.html',
        data = db_execute(query).fetchall()
    )

@app.route('/deleteAnnouncement', methods=['POST'])
def deleteAnnouncement():
    announcement = db.session.query(Announcement).filter(
        Announcement.announcement_id == request.form['announcementID']
    ).first()
    db.session.delete(announcement)
    db.session.commit()
    
    query = "SELECT * from announcement"
    return render_template('announcements.html',
        data = db_execute(query).fetchall()
    )

@login_required
@app.route("/addAnnouncement", methods=['POST'])
def addAnnouncement():
    #image = request.files['imageUpload']
    announcement = Announcement(
        title = request.form['title'], 
        description = request.form['description'], 
        date = datetime.now()
    )
    db.session.add(announcement)
    db.session.commit()
    
    query = "SELECT * from announcement"
    return render_template('announcements.html',
        data = db_execute(query).fetchall()
    )

@app.route("/showAnnouncements", methods=['GET'])
def showAnnouncements():
    query = "SELECT * from announcement"
    #images = [(base64.b64encode(item['image'] for item in result.fetchall()).DATA).encode('ascii')]
    #imagesRaw = [item['image'] for item in result.fetchall()]
    #imagesFormatted = []
    #for x in imagesRaw:
    #    imagesFormatted.append(base64.b64encode(x.DATA))
    return render_template('announcements.html',
        data = db_execute(query).fetchall()
    )



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
