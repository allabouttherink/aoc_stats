import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    AOC_URL = os.environ.get('AOC_URL') or 'https://adventofcode.com/2024/leaderboard/private/view/4238010.json'

    SESSION_KEY = os.environ.get('AOC_SESSION') or '53616c7465645f5f559e8a6ee1391c3ca45203ea7624b1f0a4e48f9c6e4a673710f09007d3ee063cee70285585805dc324fddb207b77d22b182e0835210be7b4'

    CACHE_FILE = os.path.join(BASEDIR, 'latest.json')

    READ_FROM_CACHE = False
    #READ_FROM_CACHE = True
