from utils import TweetsMongoDB
import time
import json
from tqdm import tqdm

'''
get user vectors
train rnn
train cnn
concatenation and prediction

'''


def create_user_vector_sequence(query, pop_db, pop_coll):
    records_cascade = TweetsMongoDB('tweets2').db['fixed_length_cascade']

    # # empty vector sequence lower then 5
    # records_cascade.update_many({'$or': [{'user_vector_sequence': {'$size': 1}, 'user_vector_sequence': {'$size': 2},
    #                                       'user_vector_sequence': {'$size': 3}, 'user_vector_sequence': {'$size': 4}}],
    #                              '$set': {'user_vector_sequence': []}})

    cascades = records_cascade.find(query)
    count = records_cascade.count_documents(query)

    # Create buffer variables
    buffer_user_vectors = {}

    pbar = tqdm(total=count)

    records_timeline = TweetsMongoDB(pop_db).db[pop_coll]
    try:
        for cascade in cascades:
            start_time = time.time()
            _id = cascade['_id']
            # print(cascade['user_id_sequence'], _id)
            for i, user_id in enumerate(cascade['user_id_sequence'][:5]):
                # print(user_id)
                # check if user_id is available in the buffer
                if user_id in buffer_user_vectors.keys():
                    if pop_db == 'tweets' and pop_coll == 'timeline_extended':
                        records_cascade.update_one(
                            {'_id': _id},
                            {'$push': {'user_vector_sequence': buffer_user_vectors[user_id]}})
                    elif pop_db == 'tweets2' and pop_coll == 'user_timeline_liwc':
                        records_cascade.update_one(
                            {'_id': _id},
                            {'$push': {'length_5_timeline_10': buffer_user_vectors[user_id]}})

                else:
                    if pop_db == 'tweets' and pop_coll == 'timeline_extended':
                        timeline = records_timeline.find_one({'user_id': user_id})
                    elif pop_db == 'tweets2' and pop_coll == 'user_timeline_liwc':
                        timeline = records_timeline.find_one({'user_id': str(user_id)})

                    try:

                        # # create a dynamic variable names
                        # globals()['sequence_position_%s' % i] = json.loads(timeline['timeline'][0]['user'])

                        if pop_db == 'tweets' and pop_coll == 'timeline_extended':
                            buffer_user_vectors[user_id] = timeline['timeline'][0]['user']
                        elif pop_db == 'tweets2' and pop_coll == 'user_timeline_liwc':
                            buffer_user_vectors[user_id] = timeline['length_5_timeline_10']

                        if pop_db == 'tweets' and pop_coll == 'timeline_extended':
                            records_cascade.update_one(
                                {'_id': _id},
                                {'$push': {'user_vector_sequence': timeline['timeline'][0]['user']}})
                        elif pop_db == 'tweets2' and pop_coll == 'user_timeline_liwc':
                            records_cascade.update_one(
                                {'_id': _id},
                                {'$push':
                                    {
                                        'length_5_timeline_10': timeline['length_5_timeline_10']}})

                    except IndexError:
                        buffer_user_vectors[user_id] = 0
                        records_cascade.update_one(
                            {'_id': _id},
                            {{'$push':
                                {
                                    'length_5_timeline_10': timeline['length_5_timeline_10']}}})
                    except Exception as e:
                        continue
                # print('dict len: ', len(buffer_user_vectors))
                if len(buffer_user_vectors) == 20:
                    to_be_removed_keys = list(buffer_user_vectors.keys())[:10]
                    for value in to_be_removed_keys:
                        buffer_user_vectors.pop(value)
            pbar.update(1)
            end_time = time.time()
            # print(end_time - start_time)
    except Exception as e:
        print(e)
        pbar.close()
        create_user_vector_sequence(query, pop_db, pop_coll)

    pbar.close()


def count_to_be_removed():
    records_cascade = TweetsMongoDB.db['timeline_extended']
    records = records_cascade.find({'timeline': {'$exists': True, '$size': 0}})
    count = 0
    to_be_removed = 0
    records_cascade = TweetsMongoDB.db['fixed_length_cascade']

    for record in records:
        user_id = record['user_id']
        count += 1
        to_be_removed_records = records_cascade.find({'user_id_sequence': {'$elemMatch': {'$eq': user_id}}})
        for to_be_removed_record in to_be_removed_records:
            to_be_removed += 1
    print('empty user ids: ', count)
    print('to be removed: ', to_be_removed)


def update_duplicate_sequnece():
    records_cascade = TweetsMongoDB('tweets2').db['fixed_length_cascade']
    cursor = records_cascade.aggregate(
        [
            {"$group": {"_id": "$_id_fixed_length_5", "unique_ids": {"$addToSet": "$_id"},
                        "count": {"$sum": 1}}},
            {"$match": {"count": {"$gte": 2}}}
        ]
    )

    response = []
    for doc in cursor:
        del doc["unique_ids"][0]
        for id in doc["unique_ids"]:
            response.append(id)

    # print(len(response))
    records_cascade.update_many({"_id": {"$in": response}}, {'$set': {'length_5_unique': False}})
    records_cascade.update_many({"_id": {"$nin": response}}, {'$set': {'length_5_unique': True}})


def create_sequence_id():
    records_cascade = TweetsMongoDB.db['fixed_length_cascade']
    cursor = records_cascade.find()

    for record in cursor:
        sequence = record['user_id_sequence']
        _id = record['_id']
        # print(sequence)
        _id_sequence = ''
        # sequence = list(dict.fromkeys(sequence))
        for s_id in sequence:
            _id_sequence += str(s_id)
        # print(_id_sequence)
        records_cascade.update_one(
            {'_id': _id},
            {'$set': {'_id_fixed_length_sequence': _id_sequence}})


def create_user_vector_sequence_improved():
    # improved query with 5 step buffer

    records_cascade = TweetsMongoDB.db['fixed_length_cascade']
    cascades = records_cascade.find({'user_vector_sequence.0': {'$exists': False}})

    records_timeline = TweetsMongoDB.db['timeline_extended']

    for cascade in cascades:
        for user_id in cascade['user_id_sequence']:
            timeline = records_timeline.find_one({'user_id': user_id})


if __name__ == '__main__':
    # create_user_vector_sequence({'user_vector_sequence.0': {'$exists': False}}, 'tweets', 'timeline_extended')
    create_user_vector_sequence({'length_5_timeline_10.0': {'$exists': False}}, 'tweets2', 'user_timeline_liwc')
    # create_user_vector_sequence({'length_5_timeline_10.0': {'$exists': False},
    #                              '_id_fixed_length_sequence': '137913853084103475213791385308410347521379138530841034752137913853084103475213791385308410347521379138530841034752301039688301039688301039688301039688'},
    #                             'tweets2', 'user_timeline_liwc')

    # update_duplicate_sequnece()
    # create_sequence_id()
