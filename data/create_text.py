from utils import TweetsMongoDB
from tqdm import tqdm


def create_text(query):
    records = TweetsMongoDB('tweets2').db['fixed_length_cascade']
    records_timeline = TweetsMongoDB('tweets').db['timeline_extended']
    count = records.count_documents(query)
    records = records.find(query)

    pbar = tqdm(total=count)

    for record in records:
        user_ids = record['user_id_sequence']
        user_ids = list(dict.fromkeys(user_ids))
        for user_id in user_ids:
            user_timeline = records_timeline.find_one({'user_id' : user_id})
            with open('C:/Users/Akila/Desktop/5_text/'+str(user_id)+'.txt', 'a', encoding="utf-8") as f:
                for event in user_timeline['timeline']:
                    # print(event['id'])
                    f.write(event['full_text'])
                    f.write('\n')
        pbar.update(1)


if __name__ == '__main__':
    create_text(
        {'user_vector_sequence': {'$nin': [0]}, 'user_vector_sequence.9': {'$exists': True}, 'length_5_unique': True})
