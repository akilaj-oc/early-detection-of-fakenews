from utils import TweetsMongoDB
from tqdm import tqdm
import glob
import json

def create_text():
    records = TweetsMongoDB('tweets2').db['fixed_length_cascade']
    records_timeline = TweetsMongoDB('tweets').db['timeline_extended']
    count = records.count_documents(query)
    records = records.find(query)

    pbar = tqdm(total=count, desc='Append Unique Ids')
    unique_ids = []
    for record in records:
        user_ids = record['user_id_sequence']
        user_ids = list(dict.fromkeys(user_ids))
        for user_id in user_ids:
            unique_ids.append(user_id)

        pbar.update(1)
    pbar.close()

    unique_ids = list(dict.fromkeys(unique_ids))

    # save unique_ids as a json
    with open('C:/Users/Akila/Desktop/' + folder_name + '/unique_ids.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps({"unique_ids" : unique_ids}))

    if len(created_ids) != 0:
        unique_ids = list(set(unique_ids) - set(created_ids))

    # pbar = tqdm(total=len(unique_ids), desc='Create text files')
    #
    # for unique_id in unique_ids:
    #     user_timeline = records_timeline.find_one({'user_id': unique_id})
    #     with open('C:/Users/Akila/Desktop/' + folder_name + '/' + str(unique_id) + '.txt', 'w', encoding="utf-8") as f:
    #         for event in user_timeline['timeline'][:10]:
    #             f.write(event['full_text'])
    #             f.write('\n')
    #     pbar.update(1)
    # pbar.close()


if __name__ == '__main__':
    folder_name = 'length_5_timeline_10'
    created_ids = []
    query = {'user_vector_sequence': {'$nin': [0]}, 'user_vector_sequence.5': {'$exists': True}, 'length_5_unique': True}
    for file in glob.glob('C:\\Users\\Akila\\Desktop\\' + folder_name + '\\*.txt'):
        created_ids.append(int(file[24 + len(folder_name):-4]))

    try:
        create_text()
    except Exception as e:
        print(e)
        # raise e
        create_text()
