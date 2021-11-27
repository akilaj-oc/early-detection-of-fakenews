from pymongo import MongoClient


class TweetsMongoDB(object):
    # connect to mongoDB
    _client = MongoClient('mongodb://localhost:27017/')
    db = _client.get_database('tweets')