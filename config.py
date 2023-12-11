import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')

class Config(object):
    SESSION_KEY = os.environ.get('AOC_SESSION') or '53616c7465645f5f8d31939315e938e53412d9dc900e625682eee4fcec0c01a947f479abad84bbf28f22dda7630ef04f07ae636ed8554e49c53312f1ee029329'

    CACHE_FILE = os.path.join(BASEDIR, 'latest.json')
    READ_FROM_CACHE = False
    READ_FROM_CACHE = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DEFAULT_DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
