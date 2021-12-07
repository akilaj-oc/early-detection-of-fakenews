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
                    {'user_sequence': [node.name for node in list(leaf.path)], 'ground_truth': ground_truth})
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

                #floating index
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
        fixed_length_sequence = Cascade.transform_to_fixed_length_sequence(data['user_sequence'], fixed_length)
        print(fixed_length_sequence)

        # write to mongodb
        records = TweetsMongoDB.db['fixed_length_cascade']
        try:
            records.insert_one(
                {'user_id_sequence': fixed_length_sequence, 'ground_truth': data['ground_truth'],
                 'sequence': {'fixed_length': fixed_length}})
        except Exception as e:
            raise e


if __name__ == '__main__':
    main_create_fixed_length_cascade(5)
