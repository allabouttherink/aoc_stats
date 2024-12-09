'''Fetch and organize data from AOC endpoint'''
import os
import logging
import datetime
import requests
import json

LOG = logging.getLogger('aoc_stats')

class AOC(object):
    '''Main class for AOC data'''

    # AOC event start time (unix timestamp, EST)
    START = 1733029200

    def __init__(self, app):
        self.app = app

        # connection setup
        self.url = app.config['AOC_URL']
        self.session = app.config['SESSION_KEY']
        self.user_agent = app.config['USER_AGENT']
        if not self.url or not self.session or not self.user_agent:
            LOG.error('invalid config: url=%s, session=%s, user_agent=%s'
                            % (self.url, self.session, self.user_agent))
            raise RuntimeError('bad config')

        # cache file setup
        self.cache_file = app.config['CACHE_FILE']
        self.do_update = app.config['DATA_UPDATE']
        if not self.do_update:
            if not os.path.exists(self.cache_file):
                LOG.error('cache file missing: %s' % self.cache_file)
                raise RuntimeError('missing cache file')

            # read cache and parse
            with open(self.cache_file) as fp:
                self.data = json.load(fp)
            self.parse_data()

            # set timestamp for cached data
            self.ts = datetime.datetime.utcnow()

        # do initial update
        if self.do_update:
            self.update()

    def update(self):
        '''Fetch data from API and parse.'''
        self.fetch_data()
        self.parse_data()

        # set timestamp for freshness of data
        self.ts = datetime.datetime.utcnow()
        LOG.info('update complete - %s' % self.ts)

    def fetch_data(self):
        '''Pull data from AOC API and write it to cache file.'''
        try:
            resp = requests.get(self.url,
                    headers={'User-Agent': self.user_agent},
                    cookies={'session':self.session})
            resp.raise_for_status()
            self.data = resp.json()

            # write to cache file
            with open(self.cache_file, 'w') as fp:
                json.dump(self.data,fp,indent=2)

        except Exception as e:
            LOG.error('update() - AOC request failed')
            LOG.error(e)
            self.data = {}

    def parse_data(self):
        '''Parse users and stars from data'''
        self.users = {}
        self.stars = []

        if not self.data:
            LOG.error('no data to parse!')
            raise RuntimeError('no data to parse')

        for uid, udata in self.data["members"].items():
            uid, user = int(uid), udata['name']
            self.users[uid] = user if user is not None else 'anon%d' % uid

            for day, ddata in udata["completion_day_level"].items():
                for star, sdata in ddata.items():
                    star_ts = sdata["get_star_ts"]
                    s = Star(int(uid), user, int(day), int(star), star_ts)
                    self.stars.append(s)

    @property
    def days(self):
        '''Calculates set of days from all solved stars.'''
        return set([x.day for x in self.stars])

    @property
    def max_day(self):
        '''Calculates latest day from all solved stars.'''
        return max(self.days) if self.days else 0

    @property
    def pts_scale(self):
        '''Returns points scale for leaderboard based on number of users.'''
        return [x for x in range(len(self.users), 0, -1)]

    def get_stars(self, uids=None, days=None, idxs=None):
        '''Filter star list by user_ids, days, and/or indices.'''
        stars = self.stars

        if uids:
            stars = filter(lambda x: x.uid in uids, stars)
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

    def star_elapsed(self, star):
        '''
        Calculate solve time for a given star.

        First stars are calculated relative to the start of the given day.
        Second starts are calculated relative to the first star solve time.
        '''
        # calc from day start
        if star.idx == 1:
            day_start = self.START + (star.day-1)*(3600*24)
            day_start = datetime.datetime.utcfromtimestamp(day_start)
            rv = star.time - day_start

        # calc star2 - star1
        else:
            star1 = [x for x in self.get_stars(uids=[star.uid],
                                                days=[star.day], idxs=[1])][0]
            rv = star.time - star1.time

        return rv

class Star(object):
    '''Utility class for star management'''

    def __init__(self, uid, user, day, idx, time):
        self.uid = uid
        self.user = user
        self.day = day
        self.idx = idx
        self.time = datetime.datetime.utcfromtimestamp(time)

    def __key(self):
        return (self.uid, self.day, self.idx)

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
