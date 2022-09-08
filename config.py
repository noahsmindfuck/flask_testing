import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DB_PWD = os.environ.get('SECRET_KEY') or 'golf dowry cruelly gloater plural'
    DB_HOST = os.environ.get('SECRET_KEY') or '37.252.189.147'
    DB_USER = os.environ.get('SECRET_KEY') or 'flask_testing'
    DB_NAME = os.environ.get('SECRET_KEY') or '/flask_testing'
    userpass = 'mysql+pymysql://' + DB_USER + ':' + DB_PWD + '@'
    SQLALCHEMY_DATABASE_URI = userpass + DB_HOST + DB_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'echo_pool':'debug',
        'pool_size':10,
        'max_overflow':15
    }
