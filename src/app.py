import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_track_usage import TrackUsage
from flask_track_usage.storage.sql import SQLStorage
from flask_talisman import Talisman # To force an SSL connection
#from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
talisman = Talisman()
login_manager = LoginManager()
t = TrackUsage()
#mail = Mail()

def create_app():
    app = Flask(__name__)
     # Load config from ENV is set, default otherwise.
    app.config.from_object(os.getenv('FLASK_SETTINGS', 'config.Config'))

    # Configuring database.
    # Causes significant overhead if True.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Tracks cookies - used for unique visitor count
    app.config['TRACK_USAGE_COOKIE'] = True

    db.init_app(app)
    talisman.init_app(
        app,
        content_security_policy={
            'default-src': '\'self\'',
            'img-src': [
                '*',
                'data: https:',
            ],
            'font-src': '*',
            'script-src': [
                '\'self\'',
                '\'unsafe-inline\'',
                'maxcdn.bootstrapcdn.com',
                'cdnjs.cloudflare.com',
                'ajax.googleapis.com',
                'kit.fontawesome.com',
                'cdn.quilljs.com',
            ],
            'style-src': [
                '\'self\'',
                '\'unsafe-inline\'',
                'maxcdn.bootstrapcdn.com',
                'kit-free.fontawesome.com',
                'cdn.quilljs.com',
            ],
        }
    )
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    #mail.init_app(app)

    # We need the app's context to create the db related to it.
    from models import init_db, User
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

    @app.errorhandler(404)
    def page_not_found(error):
       return render_template('404.html', title = '404'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()