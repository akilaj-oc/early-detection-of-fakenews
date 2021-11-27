from utils import TweetsMongoDB

import json

from anytree.importer import DictImporter
from anytree import PreOrderIter


# create cascades
class Cascade(object):
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
