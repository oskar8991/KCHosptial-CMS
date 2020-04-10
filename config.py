import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Gunicorn config
bind = "0.0.0.0:5000"

# Flask config
class Config():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
    SECRET_KEY = '_5#y2L"F4Q8z\n\xec]/'

    # Flask-Mail settings
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'youremail@example.com')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'yourpassword')
    # MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '"MyApp" <noreply@example.com>')
    # MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    # MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
    # MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))


class ProductionConfig(Config): # to update when we deploy
    pass

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'