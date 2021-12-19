import  csv
import pandas as pd
from  utils import TweetsMongoDB
import json


def create_liwc_vector():
    records = TweetsMongoDB('tweets2').db['user_timeline_liwc']

    df = pd.read_csv(file_path)

    for index, row in df.iterrows():
        vector_json = row[col_names].to_json()
        vector_json = json.loads(vector_json)
        vector_json['user_id'] = vector_json['Filename'][:-4]

        vector_json = {
            'user_id' : vector_json['Filename'][:-4],
            folder_name : vector_json
        }
        del vector_json[folder_name]['Filename']
        del vector_json[folder_name]['user_id']
        # populate db
        records.insert_one(vector_json)


if __name__ == '__main__':
    folder_name = 'length_5_timeline_max'
    col_names = ['Filename', 'i', 'you_total', 'adverb', 'negate', 'number', 'see', 'hear', 'sexual', 'money', 'swear']
    file_path = r'C:\Users\Akila\Desktop\timeline\LIWC2015 Results (' +folder_name+' (2168 files)).csv'
    create_liwc_vector()