'''App config'''
import os

# JSON endpoint for AOC private leaderboard
AOC_URL="https://adventofcode.com/2024/leaderboard/private/view/4238010.json"

# AOC session key - pull from cookie
AOC_SESSION="53616c7465645f5f7dba66c5c091e4c63e24086aee523a1dbdd74fef4aa90cbc931a36f25876c3e33362e425ab9c1f0aa09a547174c00ab0737b37f47bd0df13"

# user agent string sent in all requests
AOC_USER_AGENT="john.carto@gmail.com"

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
