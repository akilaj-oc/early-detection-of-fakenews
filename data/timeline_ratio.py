from utils import TweetsMongoDB
from collections import Counter

def get_root_users():
    records_cascade = TweetsMongoDB('tweets2').db['fixed_length_cascade']

    cascades_true = records_cascade.find(
        {'ground_truth': True, 'meta.unique_id_count': {'$gte': 1}, 'user_vector_sequence': {'$nin': [0]},
         'user_vector_sequence': {'$size': 10}})
    cascades_false = records_cascade.find(
        {'ground_truth': False, 'meta.unique_id_count': {'$gte': 1}, 'user_vector_sequence': {'$nin': [0]},
         'user_vector_sequence': {'$size': 10}})

    root_users_true = list(dict.fromkeys([cascade['root']['user_id'] for cascade in cascades_true]))
    root_users_false = list(dict.fromkeys([cascade['root']['user_id'] for cascade in cascades_false]))

    root_users_true = [str(val) for val in root_users_true]
    root_users_false = [str(val) for val in root_users_false]

    return root_users_true, root_users_false

def get_spreaders():
    records_cascade = TweetsMongoDB('tweets2').db['fixed_length_cascade']

    cascades_true = records_cascade.find(
        {'ground_truth': True, 'meta.unique_id_count': {'$gte': 1}, 'user_vector_sequence': {'$nin': [0]},
         'user_vector_sequence': {'$size': 10}})
    cascades_false = records_cascade.find(
        {'ground_truth': False, 'meta.unique_id_count': {'$gte': 1}, 'user_vector_sequence': {'$nin': [0]},
         'user_vector_sequence': {'$size': 10}})

    root_users_true = [list(dict.fromkeys(cascade['user_id_sequence']) ) for cascade in cascades_true]
    root_users_false = [list(dict.fromkeys(cascade['user_id_sequence']) ) for cascade in cascades_false]

    root_users_true = list(dict.fromkeys([item for elem in root_users_true for item in elem]))
    root_users_false = list(dict.fromkeys([item for elem in root_users_false for item in elem]))

    root_users_true = [str(val) for val in root_users_true]
    root_users_false = [str(val) for val in root_users_false]

    return root_users_true, root_users_false


def create_sum_timeline(root_users_true, root_users_false):
    records_cascade = TweetsMongoDB('tweets2').db['user_timeline_liwc']
    cursor_true = records_cascade.find({'user_id' : {'$in' : root_users_true}})
    cursor_false = records_cascade.find({'user_id' : {'$in' : root_users_false}})
    count_true = records_cascade.count_documents({'user_id' : {'$in' : root_users_true}})
    count_false = records_cascade.count_documents({'user_id' : {'$in' : root_users_false}})
    sum_dict_true = {}
    sum_dict_false = {}

    for record in cursor_true:
        sum_dict_true = Counter(sum_dict_true) + Counter(record['length_5_timeline_max'])

    for record in cursor_false:
        sum_dict_false = Counter(sum_dict_false) + Counter(record['length_5_timeline_max'])

    sum_dict_true = {k: float(sum_dict_true[k]) / count_true for k in sum_dict_false}
    sum_dict_false = {k: float(sum_dict_false[k]) / count_false for k in sum_dict_false}

    ratio_dict = {k: float(sum_dict_false[k])/sum_dict_true[k] for k in sum_dict_false}

    return ratio_dict

if __name__ == '__main__':
    root_users_true, root_users_false = get_root_users()
    print(create_sum_timeline(root_users_true, root_users_false))

    root_users_true, root_users_false = get_spreaders()
    print(create_sum_timeline(root_users_true, root_users_false))




