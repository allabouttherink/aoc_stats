import datetime
import requests
import json
from collections import defaultdict

import logging
logger = logging.getLogger('aoc_stats')
gunicorn_error_logger = logging.getLogger('gunicorn.error')
logger.handlers.extend(gunicorn_error_logger.handlers)
logger.setLevel(logging.DEBUG)

AOC_URL = 'https://adventofcode.com/2023/leaderboard/private/view/2258949.json'

class AOC(object):

    def __init__(self, app):
        self.app = app
        self.session = app.config['SESSION_KEY']
        self.cache_file = app.config['CACHE_FILE']
        self.read_cache = app.config['READ_FROM_CACHE']

        if self.read_cache:
            with open(self.cache_file) as fp:
                self.cache_data = json.load(fp)

        # initial update
        self.update()

    def update(self):
        try:
            if self.read_cache:
                self.data = self.cache_data
            else:
                resp = requests.get(AOC_URL, cookies={'session':self.session})
                resp.raise_for_status()
                self.data = resp.json()

                with open(self.cache_file, 'w') as fp:
                    json.dump(self.data,fp,indent=2)

        except:
            logger.error('AOC request failed')
            self.data = {}

        self.ts = datetime.datetime.utcnow()

        # parse data
        self.users = set()
        self.stars = []
        for uid, udata in self.data["members"].items():
            user = udata["name"]
            self.users.add(user)
            for day, ddata in udata["completion_day_level"].items():
                for star, sdata in ddata.items():
                    s = Star(user, int(day), int(star), sdata["get_star_ts"])
                    self.stars.append(s)

    @property
    def days(self):
        return set([x.day for x in self.stars])

    @property
    def pts_scale(self):
        return [x for x in range(len(self.users), 0, -1)]

    def get_stars(self, users=None, days=None, idxs=None):
        '''Filter star list.'''
        stars = self.stars

        if users:
            stars = filter(lambda x: x.user in users, stars)
        if days:
            stars = filter(lambda x: x.day in days, stars)
        if idxs:
            stars = filter(lambda x: x.idx in idxs, stars)

        return stars

    def get_star_points(self, day, idx):
        '''Calculate points for a particular star.'''
        stars = sorted(self.get_stars(days=[day], idxs=[idx]))
        return {star:self.pts_scale[idx] for idx,star in enumerate(stars)}

    def get_day_points(self, day):
        '''Calculate points for all stars on a particular day.'''
        pts_map = {}
        for x in [1, 2]:
            pts_map.update(self.get_star_points(day, x))
        return pts_map

    def get_all_points(self):
        '''Calculate points for all stars.'''
        pts_map = {}
        for day in self.days:
            pts_map.update(self.get_day_points(day))
        return pts_map


class Star(object):
    def __init__(self, user, day, idx, time):
        self.user = user if not None else 'Anonymous'
        self.day = day
        self.idx = idx
        self.time = datetime.datetime.fromtimestamp(time)

    def __key(self):
        return (self.user, self.day, self.idx)

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        if isinstance(other, A):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
            return 'Star(%s, %d, %d)' % self.__key()
    def __repr__(self):
            return 'Star(%s, %d, %d)' % self.__key()
