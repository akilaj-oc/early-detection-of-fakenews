from utils import TweetsMongoDB

import json
import glob

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


def main():
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


if __name__ == '__main__':
    main()
