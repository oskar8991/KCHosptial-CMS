#from medications import medicationsList, generateChart
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
#db.metadata.reflect(engine=engine)


# TrackUsage Setup
pstore = SQLStorage(db=db)
t = TrackUsage(app, [pstore])