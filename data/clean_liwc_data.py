import  csv
import pandas as pd
from  utils import TweetsMongoDB
import json


def test():
    file = open(r'C:\Users\Akila\Desktop\timeline\LIWC2015 Results (length_5_timeline_10 (2168 files)).csv')
    print(type(file))
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    print(header)

    rows = []
    for row in csvreader:
        rows.append(row)
    print(rows[:10])
    pandas_dataframe = pd.DataFrame(rows)
    zero_col = (pandas_dataframe == 0).sum(axis=0)
    print(zero_col)


def main():
    col_names = ['Filename', 'i', 'you_total', 'adverb', 'negate', 'number', 'see', 'hear', 'sexual', 'money', 'swear']
    df = pd.read_csv(r'C:\Users\Akila\Desktop\timeline\LIWC2015 Results (length_5_timeline_10 (2168 files)).csv')
    print(df.head())
    print(df.loc[df['Filename'] == '1000530532864790528.txt'][col_names])
    for index, row in df.iterrows():
        # print(row[col_names].to_json())
        vector_json = row[col_names].to_json()
        vector_json = json.loads(vector_json)
        vector_json['user_id'] = vector_json['Filename'][:-4]
        del vector_json['Filename']
        print(vector_json)


def create_liwc_vector():
    records = TweetsMongoDB('tweets2').db['user_timeline_liwc']

    df = pd.read_csv(file_path)

    for index, row in df.iterrows():
        vector_json = row[col_names].to_json()
        vector_json = json.loads(vector_json)
        vector_json['user_id'] = vector_json['Filename'][:-4]

        vector_json = {
            'user_id' : vector_json['Filename'][:-4],
            'length_5_timeline_10' : vector_json
        }
        del vector_json['length_5_timeline_10']['Filename']
        del vector_json['length_5_timeline_10']['user_id']
        # populate db
        records.insert_one(vector_json)


if __name__ == '__main__':
    col_names = ['Filename', 'i', 'you_total', 'adverb', 'negate', 'number', 'see', 'hear', 'sexual', 'money', 'swear']
    file_path = r'C:\Users\Akila\Desktop\timeline\LIWC2015 Results (length_5_timeline_10 (2168 files)).csv'
    create_liwc_vector()