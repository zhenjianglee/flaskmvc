import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 465
    MAIL_USERNAME =  os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = 'ECHO'
    MAIL_SENDER = 'Hiya76 <hiya76@sina.com>'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir,'db-dev.sqlite')


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI=os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir,'db-test.sqlite')

class LiveConfig(Config):

    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir,'db.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing':TestConfig,
    'production':LiveConfig,
    'default':DevelopmentConfig
}


