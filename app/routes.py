from flask import render_template, abort
from app import app, scheduler, charts
from app import aoc as AOC
import logging
import datetime
logger = logging.getLogger('aoc_stats')

@scheduler.task('interval', id='data_update', seconds=15)
def data_update():
    app.aoc.update()

@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html', title='400 - Bad Request'), 400

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='404 - File Not Found'), 404

@app.errorhandler(500)
def not_found_error(error):
    return render_template('500.html', title='500 - Internal Server Error'), 500

@app.template_filter('max')
def template_max(it):
    return max(it)

@app.template_filter('star_elapsed')
def template_star_elapsed(star):

    day_start = app.aoc.START + (star.day-1)*(3600*24)
    day_start = datetime.datetime.utcfromtimestamp(day_start)

    return star.time - day_start
    #else:
    #    star1 = [x for x in app.aoc.get_stars(uids=[star.uid], days=[star.day], idxs=[1])][0]
    #    return star.time - star1.time

@app.route('/')
@app.route('/index')
def index():

    aoc = app.aoc
    stars = aoc.get_all_points()

    # user stats
    users = []
    for uid in aoc.users:
        ustars = [s for s in filter(lambda x: x.uid == uid, stars)]
        pts = sum(stars[s] for s in ustars)
        smap = {d:len([x for x in filter(lambda x: x.day == d, ustars)]) for d in aoc.days}
        extra = 0

        # calc remaining pts
        for d in aoc.days:
            for x in [1, 2]:
                ds = [d for d in aoc.get_stars(days=[d], idxs=[x])]
                s = [y for y in filter(lambda x: x.uid == uid, ds)]
                extra += aoc.pts_scale[len(ds)] if len(s) == 0 else 0


        users.append({
            'uid': uid,
            'user':aoc.users[uid],
            'pts': pts,
            'max_pts': pts + extra,
            'num_stars': len(ustars),
            'stars': smap
            })
        users = sorted(users, key=lambda x: x['pts'], reverse=True)

    # cum chart
    csum_chart = charts.get_csum_chart(aoc)

    return render_template('index.html', aoc=app.aoc, csum_chart=csum_chart,
            users=users)

@app.route('/user/<uid>')
def user_page(uid):

    aoc = app.aoc

    try:
        uid = int(uid)
        if uid not in aoc.users:
            abort(404)
        user = aoc.users[uid]
    except ValueError:
        abort(400)

    stars = {(x.day,x.idx):x for x in aoc.get_stars(uids=[uid])}

    return render_template('user.html', aoc=aoc, stars=stars, user=user)
