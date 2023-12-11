from flask import render_template
from app import app, scheduler, charts

import logging
logger = logging.getLogger('aoc_stats')

@scheduler.task('interval', id='data_update', seconds=15)
def data_update():
    app.aoc.update()

@app.route('/')
@app.route('/index')
def index():

    aoc = app.aoc
    stars = aoc.get_all_points()
    user_pts = {}

    for user in aoc.users:
        ustars = filter(lambda x: x.user == user, stars)
        user_pts[user] = sum([stars[s] for s  in ustars])

 #   for user in sorted(user_pts, key=lambda x: user_pts[x], reverse=True):
 #       print('%s: %d' % (user, user_pts[user]))


    # cum chart
    csum_chart = charts.get_csum_chart(aoc)
    #print(csum_chart[0])

    return render_template('index.html', aoc=app.aoc, csum_chart=csum_chart)
