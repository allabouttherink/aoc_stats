'''Utility functions to generate chart data.'''

COLORS = [
    'rgb(255, 0, 41)',
    'rgb(55, 126, 184)',
    'rgb(102, 166, 30)',
    'rgb(152, 78, 163)',
    'rgb(0, 210, 213)',
    'rgb(255, 127, 0)',
    'rgb(175, 141, 0)',
    'rgb(127, 128, 205)',
    'rgb(179, 233, 0)',
    'rgb(196, 46, 96)',
]

def get_csum_chart(aoc):

    stars = aoc.get_all_points()
    user_pts = {}
    chart = []

    # build data
    for n,uid in enumerate(aoc.users):
        ustars = filter(lambda x: x.uid== uid, stars)
        udata = []
        uinfo = []
        pts = 0

        # cumulative sum
        for star in sorted(ustars):
            pts += stars[star]
            udata.append({'x': star.time, 'y': pts})
            uinfo.append({'day': star.day, 'idx': star.idx})

        chart.append({
            'label': aoc.users[uid],
            'backgroundColor': COLORS[n % len(COLORS)],
            'data': udata,
            'uinfo': uinfo
        })

    return chart

def get_whisker_chart(aoc):

    days = sorted(aoc.days)
    chart = {
        'days': days,
        'star1': [],
        'star2': []
    }

    for d in days:
        for idx in [1,2]:
            stars = aoc.get_stars(days=[d], idxs=[idx])
            deltas = [aoc.star_elapsed(s) for s in stars]
            chart['star%d' % idx].append([s.total_seconds()/60.0 for s in deltas])

    return chart
