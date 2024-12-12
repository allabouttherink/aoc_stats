'''App config'''
import os

# JSON endpoint for AOC private leaderboard
AOC_URL=""

# AOC session key - pull from cookie
AOC_SESSION=""

# user agent string sent in all requests
AOC_USER_AGENT=""

class Config(object):
    '''Read config from environment or use defaults'''

    # AOC connection info
    AOC_URL = os.environ.get('AOC_URL') or AOC_URL
    SESSION_KEY = os.environ.get('AOC_SESSION') or AOC_SESSION
    USER_AGENT = os.environ.get('AOC_USER_AGENT') or AOC_USER_AGENT

    # data file
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    CACHE_FILE = os.path.join(BASEDIR, 'data', 'latest.json')

    # set to False for testing - will not update data and just read from cache
    DATA_UPDATE = True
    #DATA_UPDATE = False
