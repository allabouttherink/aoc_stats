'''Content generation for HTTP endpoints.'''
import logging
import datetime

from flask import render_template, abort

from app import app, charts

LOG = logging.getLogger('aoc_stats')

@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html', title='400 - Bad Request'), 400

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='404 - File Not Found'), 404

@app.errorhandler(500)
def not_found_error(error):
    return render_template('500.html', title='500 - Internal Server Error'), 500

@app.route('/')
@app.route('/index')
def index():
    '''Landing page.'''
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

    # charts
    csum_chart = charts.get_csum_chart(aoc)
    whisker_chart = charts.get_whisker_chart(aoc)

    # latest stars (last 10)
    latest_stars = sorted(aoc.get_stars(), reverse=True)[:10]

    return render_template('index.html', aoc=app.aoc, csum_chart=csum_chart,
            users=users, wchart=whisker_chart, latest_stars=latest_stars)

@app.route('/user/<uid>')
def user_page(uid):
    '''Per-user statistics page.'''
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

#
# template helpers
#
@app.template_filter('max')
def template_max(it):
    return max(it)

@app.template_filter('star_elapsed')
def template_star_elapsed(star):
    return app.aoc.star_elapsed(star)
