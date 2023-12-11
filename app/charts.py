
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
    for n,user in enumerate(aoc.users):
        ustars = filter(lambda x: x.user == user, stars)
        udata = []
        uinfo = []
        pts = 0

        # cumulative sum
        for star in sorted(ustars):
            pts += stars[star]
            udata.append({'x': star.time, 'y': pts})
            uinfo.append({'day': star.day, 'idx': star.idx})

        chart.append({
            'label': user,
            'backgroundColor': COLORS[n % len(COLORS)],
            'data': udata,
            'uinfo': uinfo
        })

    return chart

#def get_csum_chart(aoc):
#
#    stars = aoc.get_all_points()
#    user_pts = {}
#    data = {}
#
#    # build data
#    for user in aoc.users:
#        ustars = filter(lambda x: x.user == user, stars)
#        data[user] = []
#        pts = 0
#
#        for star in sorted(ustars):
#            pts += stars[star]
#            data[user].append({'x': star.time, 'y': pts})
#
#    # gen chart
#    chart = []
#    for n, user in enumerate(data):
#        chart.append({
#            'label': user,
#            'backgroundColor': COLORS[n % len(COLORS)],
#            'data': data[user]
#        })
#
#    return chart
