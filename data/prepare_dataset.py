from utils import TweetsMongoDB

from collections import Counter
from utils import User
from utils import Timeline
import json
from tqdm import tqdm
import time

from collections import Counter


def add_unique_id_count():
    cascades = records_cascade.find()
    for cascade in cascades:
        _id = cascade['_id']
        user_id_sequence = cascade['user_id_sequence']
        id_count = len(Counter(user_id_sequence))
        records_cascade.update_one(
            {'_id': _id},
            {'$set': {'meta.unique_id_count': id_count}})


def create_user_vector_to_list(query):
    results = []
    cascades = records_cascade.find(query)
    for cascade in cascades:
        _id = cascade['_id']
        user_vector_sequence = cascade['user_vector_sequence']
        length_5_timeline_10 = cascade['length_5_timeline_10']
        rating = cascade['ground_truth']
        user_id = cascade['user_id_sequence'][0]

        engaged_users_vector = []
        for i in range(5):
            engaged_users_vector.append(User(user_vector_sequence[i]).vector.tolist() + Timeline(length_5_timeline_10[i]).vector.tolist())


        # engaged_users_vector = [User(user).vector.tolist() for user in user_vector_sequence[:5]]
        # length_5_timeline_10_vector = [Timeline(timeline).vector.tolist() for timeline in length_5_timeline_10[:5]]
        # print(engaged_users_vector)
        if rating:
            rating = 1
        else:
            rating = 0

        if engaged_users_vector:
            results.append((engaged_users_vector, rating, user_id))

        # print(results)

    return results


def main():
    cascades_true = records_cascade.count_documents(
        {'ground_truth': True, 'meta.unique_id_count': {'$gte': 1}, 'user_vector_sequence': {'$nin': [0]},
         'user_vector_sequence': {'$size': 10}})
    cascades_false = records_cascade.count_documents(
        {'ground_truth': False, 'meta.unique_id_count': {'$gte': 1}, 'user_vector_sequence': {'$nin': [0]},
         'user_vector_sequence': {'$size': 10}})
    print('True: ', cascades_true)
    print('False: ', cascades_false)

    cascades_true = records_cascade.find(
        {'ground_truth': True, 'meta.unique_id_count': {'$gte': 1}, 'user_vector_sequence': {'$nin': [0]},
         'user_vector_sequence': {'$size': 10}})
    cascades_false = records_cascade.find(
        {'ground_truth': False, 'meta.unique_id_count': {'$gte': 1}, 'user_vector_sequence': {'$nin': [0]},
         'user_vector_sequence': {'$size': 10}})
    print('True: ', dict(Counter([cascade['root']['user_id'] for cascade in cascades_true])))
    print('False: ', dict(Counter([cascade['root']['user_id'] for cascade in cascades_false])))


def create_json(query):
    results = create_user_vector_to_list(query)
    for result in tqdm(results):
        with open('dataset.json', "at", encoding="utf-8") as output:
            output.write(json.dumps(result) + "\n")


if __name__ == '__main__':
    records_cascade = TweetsMongoDB('tweets2').db['fixed_length_cascade']
    # create_json({'user_vector_sequence': {'$nin': [0]}, 'user_vector_sequence.9': {'$exists': True},
    #              '_id_fixed_length_sequence': '1379138530841034752340040091934004009193400400919340040091934004009193400400919138685154556471296113868515455647129611386851545564712961'})
    create_json(
        {'user_vector_sequence': {'$nin': [0]}, 'length_5_timeline_10.4': {'$exists': True}, 'length_5_unique': True})
    for i in range(5):
        create_json(
            {'user_vector_sequence': {'$nin': [0]}, 'length_5_timeline_10.4': {'$exists': True}, 'ground_truth': True,
             'length_5_unique': True})
    # main()
