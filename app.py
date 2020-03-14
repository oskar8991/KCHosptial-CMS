from flask import Flask, g, url_for, redirect, render_template, request, \
    session, abort, flash, Response, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
from sqlalchemy import *
from datetime import datetime, timedelta


from flask_track_usage import TrackUsage
from flask_track_usage.storage.sql import SQLStorage
from flask_track_usage.storage.mongo import MongoEngineStorage
from flask_track_usage.summarization import sumRemote, sumUrl, sumUserAgent

from setup import app, db, login_manager, engine, meta, pstore
from models import User, Content, flask_usage, Announcement

db.create_all()
from drug_chart.routes import drug_chart
from users.routes import users
from main.routes import main
app.register_blueprint(drug_chart)
app.register_blueprint(users)
app.register_blueprint(main)


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
    first_page = Content.query.get(1)

    if first_page:
        first_page.content = request.form["editBox"]
        db.session.commit()
    
    return redirect(url_for('main.index'))

@app.route('/edit')
#content table query for Edit.html
def retrieveContentEdit():
    return render_template('edit.html', content=Content.query.get(1).content)


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
    return render_template('users.html', data = User.query.all())

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




@app.route('/addAnnouncementPage')
def addAnnouncementPage():
    return render_template('announcements/create.html')

@app.route('/editAnnouncementPage')
def editAnnouncementPage():
    return render_template('announcements/edit.html',
        id = request.args.get('id'),
        title = request.args.get('description'),
        description = request.args.get('description')
    )

@app.route('/deleteAnnouncementPage')
def deleteAnnouncementPage():
    return render_template('announcements/delete.html',
        id = request.args.get('id'),
        title = request.args.get('title'),
        description = request.args.get('description')
    )

@app.route('/editAnnouncement', methods=['POST'])
def editAnnouncement():
    announcement = Announcement.query.get(int(request.form['announcementID']))

    if announcement:
        announcement.title = request.form['newTitle']
        announcement.description = request.form['newDescription']
        db.session.commit()
    
    return redirect(url_for('main.announcements'))

@app.route('/deleteAnnouncement', methods=['POST'])
def deleteAnnouncement():
    announcement = Announcement.query.get(int(request.form['announcementID']))
    if announcement:
        db.session.delete(announcement)
        db.session.commit()
    
    return redirect(url_for('main.announcements'))

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
    
    return redirect(url_for('main.announcements'))


if __name__ == '__main__':
    app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
