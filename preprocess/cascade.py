from utils import TweetsMongoDB

import json
import glob
import numpy as np

from anytree.importer import DictImporter
from anytree import PreOrderIter


class Cascade(object):
    # create cascades
    @staticmethod
    def create_cascade(file_name, ground_truth):
        # read json
        file = open(file_name)
        data = json.load(file)

        importer = DictImporter()
        tree = importer.import_(data)

        # write to mongodb
        records = TweetsMongoDB.db['cascades']

        for leaf in PreOrderIter(tree, filter_=lambda node: node.is_leaf):
            try:
                records.insert_one(
                    {'user_id_sequence': [node.name for node in list(leaf.path)], 'ground_truth': ground_truth,
                     'root': {'created_at': leaf.root.created_at, 'user_id': leaf.root.name}})
            except Exception as e:
                raise e

    @staticmethod
    def transform_to_fixed_length_sequence(sequence, fixed_length):
        """
        Algorithm logic.

        let P be variable length sequence
        let S be fixed length sequence where S length is n time-steps
        if P length is > n:
            truncated from last
        if P length is < n:
            randomly over-sample
        """
        if len(sequence) >= fixed_length:
            sequence = sequence[:fixed_length]
        else:
            length_difference = fixed_length - len(sequence)

            # maintain an independent incidents by maintaining a sequence copy
            sequence_copy = sequence.copy()
            random_index_change = np.zeros(len(sequence_copy))

            for value in np.ones(length_difference):
                random_index = np.random.randint(0, len(sequence_copy))

                # floating index
                random_index_change[random_index] += 1
                random_index_change_sum = sum(random_index_change[:random_index])

                sequence.insert(random_index + int(random_index_change_sum), sequence_copy[random_index])

        return sequence


def main_create_cascade():
    for file in glob.glob(r'..\data\*.json'):
        # extract ground truth
        ground_truth = file.split('_')[1]
        print(file)

        # assign a boolean value
        if ground_truth == 'true':
            ground_truth = True
        elif ground_truth == 'false':
            ground_truth = False

        print(ground_truth)

        # populate database
        Cascade.create_cascade(file, ground_truth)


def main_create_fixed_length_cascade(fixed_length):
    records = TweetsMongoDB.db['cascades']
    records = records.find()

    for data in records:
        # print(data)

        fixed_length_sequence = Cascade.transform_to_fixed_length_sequence(data['user_id_sequence'], fixed_length)

        # write to mongodb
        records = TweetsMongoDB.db['fixed_length_cascade']
        try:
            records.insert_one(
                {'user_id_sequence': fixed_length_sequence,
                 'ground_truth': data['ground_truth'],
                 'meta': {'fixed_length': fixed_length, 'unique_id_count': data['meta']['unique_id_count'],
                          '_id_sequence': data['meta']['_id_sequence']},
                 'root': {'created_at': data['root']['created_at'], 'user_id': data['root']['user_id']}})
        except Exception as e:
            raise e


def create_sequence_id(fixed_length):
    records_cascade = TweetsMongoDB('tweets2').db['fixed_length_cascade']
    cursor = records_cascade.find()

    for record in cursor:
        sequence = record['user_id_sequence']
        _id = record['_id']
        # print(sequence)
        _id_sequence = ''
        for s_id in sequence[:fixed_length]:
            _id_sequence += str(s_id)
        # print(_id_sequence)
        records_cascade.update_one(
            {'_id': _id},
            {'$set': {'_id_fixed_length_' + str(fixed_length): _id_sequence}})


def copy():
    records_cascade = TweetsMongoDB.db['fixed_length_cascade']
    records2_cascade = Tweets2MongoDB.db['cascades']
    cursor = records_cascade.find()

    for record in cursor:
        _id = record['_id']
        cursor2 = records2_cascade.find_one({'meta._id_sequence': record['meta']['_id_sequence']})
        try:
            records_cascade.update_one({'_id': _id}, {'$set': {'root': {'created_at': cursor2['root']['created_at']}}})
        except TypeError as e:
            print(record['meta']['_id_sequence'])


if __name__ == '__main__':
    # main_create_fixed_length_cascade(10)
    # main_create_cascade()
    create_sequence_id(5)
    # copy()
