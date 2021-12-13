from utils import TweetsMongoDB
import time
import json

'''
get user vectors
train rnn
train cnn
concatenation and prediction

'''


def create_user_vector_sequence():
    records_cascade = TweetsMongoDB.db['fixed_length_cascade']

    # empty vector sequence lower then 5
    records_cascade.update_many({'$or': [{'user_vector_sequence': {'$size': 1}, 'user_vector_sequence': {'$size': 2},
                                          'user_vector_sequence': {'$size': 3}, 'user_vector_sequence': {'$size': 4}}],
                                 '$set': {'user_vector_sequence': []}})


    cascades = records_cascade.find({'user_vector_sequence.0': {'$exists': False}})


    # Create buffer variables
    buffer_user_vectors = {}

    records_timeline = TweetsMongoDB.db['timeline_extended']
    try:
        for cascade in cascades:
            start_time = time.time()
            _id = cascade['_id']
            print(cascade['user_id_sequence'], _id)
            for i, user_id in enumerate(cascade['user_id_sequence']):

                # check if user_id is available in the buffer
                if user_id in buffer_user_vectors.keys():
                    records_cascade.update_one(
                        {'_id': _id},
                        {'$push': {'user_vector_sequence': buffer_user_vectors[user_id]}})
                else:
                    timeline = records_timeline.find_one({'user_id': user_id})
                    # print(timeline['timeline'][0]['user']['name'])
                    try:

                        # # create a dynamic variable names
                        # globals()['sequence_position_%s' % i] = json.loads(timeline['timeline'][0]['user'])

                        buffer_user_vectors[user_id] = timeline['timeline'][0]['user']

                        records_cascade.update_one(
                            {'_id': _id},
                            {'$push': {'user_vector_sequence': timeline['timeline'][0]['user']}})
                    except IndexError:
                        buffer_user_vectors[user_id] = 0
                        records_cascade.update_one(
                            {'_id': _id},
                            {'$push': {'user_vector_sequence': 0}})
                    except Exception as e:
                        continue
                # print('dict len: ', len(buffer_user_vectors))
                if len(buffer_user_vectors) == 10:
                    to_be_removed_keys = list(buffer_user_vectors.keys())[:5]
                    for value in to_be_removed_keys:
                        buffer_user_vectors.pop(value)

            end_time = time.time()
            print(end_time - start_time)
    except Exception as e:
        print(e)
        create_user_vector_sequence()


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


def remove_duplicate_sequnece():
    records_cascade = TweetsMongoDB.db['fixed_length_cascade']
    cursor = records_cascade.aggregate(
        [
            {"$group": {"_id": "$_id_sequence", "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gte": 2}}}
        ]
    )

    response = []
    for doc in cursor:
        del doc["unique_ids"][0]
        for id in doc["unique_ids"]:
            response.append(id)

    duplicates = []
    for _id in response:
        r = records_cascade.find_one({'_id': _id})
        duplicates.append(r['_id_sequence'])

    my_dict = {i: duplicates.count(i) for i in duplicates}
    print(len(response))
    # records_cascade.remove({"_id": {"$in": response}})


def create_sequence_id():
    records_cascade = TweetsMongoDB.db['fixed_length_cascade']
    cursor = records_cascade.find()

    for record in cursor:
        sequence = record['user_id_sequence']
        _id = record['_id']
        print(sequence)
        _id_sequence = ''
        for s_id in sequence:
            _id_sequence += str(s_id)
        print(_id_sequence)
        records_cascade.update_one(
            {'_id': _id},
            {'$set': {'_id_sequence': _id_sequence}})


def create_user_vector_sequence_improved():
    # improved query with 5 step buffer

    records_cascade = TweetsMongoDB.db['fixed_length_cascade']
    cascades = records_cascade.find({'user_vector_sequence.0': {'$exists': False}})

    records_timeline = TweetsMongoDB.db['timeline_extended']

    for cascade in cascades:
        for user_id in cascade['user_id_sequence']:
            timeline = records_timeline.find_one({'user_id': user_id})


if __name__ == '__main__':
    create_user_vector_sequence()
    # remove_duplicate_sequnece()
    # create_sequence_id()
