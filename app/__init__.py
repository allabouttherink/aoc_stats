from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_apscheduler import APScheduler

from config import Config

from . import aoc

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.aoc = aoc.AOC(app)

scheduler = APScheduler()
#scheduler.init_app(app)
scheduler.start()

from app import routes
