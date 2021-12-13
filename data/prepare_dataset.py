from utils import TweetsMongoDB

from collections import Counter
from utils import User
import json
from tqdm import tqdm


def add_unique_id_count():
    cascades = records_cascade.find()
    for cascade in cascades:
        _id = cascade['_id']
        user_id_sequence = cascade['user_id_sequence']
        id_count = len(Counter(user_id_sequence))
        records_cascade.update_one(
            {'_id': _id},
            {'$set': {'sequence.unique_id_count': id_count}})


def create_user_vector_to_list(limit, ground_truth, gte):
    results = []
    cascades = records_cascade.find({'ground_truth': ground_truth, 'sequence.unique_id_count': {'$gte': gte},
                                     'user_vector_sequence': {'$nin': [0]}})
    for cascade in cascades[:limit]:
        _id = cascade['_id']
        user_vector_sequence = cascade['user_vector_sequence']
        rating = cascade['ground_truth']
        user_id = cascade['user_id_sequence'][0]

        engaged_users_vector = [User(user).vector.tolist() for user in user_vector_sequence]

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
        {'ground_truth': True, 'sequence.unique_id_count': {'$gte': 3}, 'user_vector_sequence': {'$nin': [0]},
         'user_vector_sequence': {'$size': 5}})
    cascades_false = records_cascade.count_documents(
        {'ground_truth': False, 'sequence.unique_id_count': {'$gte': 5}, 'user_vector_sequence': {'$nin': [0]},
         'user_vector_sequence': {'$size': 5}})
    print('True: ', cascades_true)
    print('False: ', cascades_false)


def create_json():
    cascade_count = 80
    results = create_user_vector_to_list(cascade_count, True, 3)
    for result in tqdm(results):
        with open('dataset.json', "at", encoding="utf-8") as output:
            output.write(json.dumps(result) + "\n")
    results = create_user_vector_to_list(cascade_count, False, 5)
    for result in tqdm(results):
        with open('dataset.json', "at", encoding="utf-8") as output:
            output.write(json.dumps(result) + "\n")


if __name__ == '__main__':
    records_cascade = TweetsMongoDB.db['fixed_length_cascade']
    create_json()
