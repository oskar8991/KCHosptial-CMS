from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import create_engine, MetaData

from flask_track_usage import TrackUsage
from flask_track_usage.storage.sql import SQLStorage

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuring database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    # Causes significant overhead if True.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Tracks cookies - used for unique visitor count
    app.config['TRACK_USAGE_COOKIE'] = True

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'


    from models import User, init_db
    with app.app_context():
        init_db()
        # TrackUsage Setup
        pstore = SQLStorage(db=db)
        t = TrackUsage(app, [pstore])

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from drug_chart.routes import drug_chart
    from users.routes import users
    from main.routes import main
    from announcements.routes import announcements
    from faq.routes import faq
    from about.routes import about
    from content.routes import content
    from dashboard.routes import dashboard
    from quiz.routes import quiz

    blueprints = [drug_chart, users, main, faq, about, announcements, content,
        dashboard, quiz
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        t.include_blueprint(blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()