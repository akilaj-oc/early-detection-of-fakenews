from pymongo import MongoClient
import numpy as np
from datetime import datetime


class TweetsMongoDB(object):
    def __init__(self, db_name):
        self.db_name = db_name
        # connect to mongoDB
        _client = MongoClient('mongodb://localhost:27017/')
        self.db = _client.get_database(self.db_name)



class User(object):
    def __init__(self, user):
        self.user = user
        super(User, self).__init__()

    @property
    def vector(self):
        return np.array([self.length_of_user_description,
                         self.length_of_username,
                         self.followers_count,
                         self.friends_count,
                         self.statuses_count,
                         self.registration_age,
                         self.is_verified,
                         self.is_geo_enabled])

    @property
    def length_of_user_description(self):
        try:
            if self.user['description']:
                return len(self.user['description'])
            else:
                return 0
        except TypeError as e:
            print(self.user['id'])

    @property
    def length_of_username(self):
        return len(self.user['screen_name'])

    @property
    def followers_count(self):
        return self.user['followers_count']

    @property
    def friends_count(self):
        return self.user['friends_count']

    @property
    def statuses_count(self):
        return self.user['statuses_count']

    @property
    def registration_age(self):
        now = datetime.now()
        created_at = datetime.strptime(self.user['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        days = (now - created_at).days

        return days

    @property
    def is_verified(self):
        # verified: 1
        # not verified: 0

        return 1 if self.user['verified'] else 0

    @property
    def is_geo_enabled(self):
        # enabled: 1
        # not enabled: 0
        return 1 if self.user['geo_enabled'] else 0


class Timeline(object):
    def __init__(self, timeline):
        self.timeline = timeline
        super(Timeline, self).__init__()

    @property
    def vector(self):
        return np.array([self.get_i,
                         self.get_you_total,
                         self.get_adverb,
                         self.get_negate,
                         self.get_number,
                         self.get_see,
                         self.get_hear,
                         self.get_sexual,
                         self.get_money,
                         self.get_swear])


    @property
    def get_i(self):
        return self.timeline['i']

    @property
    def get_you_total(self):
        return self.timeline['you_total']

    @property
    def get_adverb(self):
        return self.timeline['adverb']

    @property
    def get_negate(self):
        return self.timeline['negate']

    @property
    def get_number(self):
        return self.timeline['number']

    @property
    def get_see(self):
        return self.timeline['see']

    @property
    def get_hear(self):
        return self.timeline['hear']

    @property
    def get_sexual(self):
        return self.timeline['sexual']

    @property
    def get_money(self):
        return self.timeline['money']

    @property
    def get_swear(self):
        return self.timeline['swear']




class bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
