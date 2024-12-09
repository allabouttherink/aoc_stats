'''App initializaton'''
import logging

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_apscheduler import APScheduler

from config import Config

# init logging
logger = logging.getLogger('aoc_stats')
logger.setLevel(logging.DEBUG)
gunicorn_error_logger = logging.getLogger('gunicorn.error')
logger.handlers.extend(gunicorn_error_logger.handlers)

# init flask app
app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
moment = Moment(app)
scheduler = APScheduler()
scheduler.start()

# init AOC
from . import aoc
app.aoc = aoc.AOC(app)
from . import routes

@scheduler.task('interval', id='data_update', seconds=900)
def data_update():
    if app.aoc.do_update:
        app.aoc.update()
