import json
from kafka import KafkaConsumer
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db.dbwrite import DBWrite

from db.dbconnect import DBConnect

def exists(obj, chain):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    _key = chain.pop(0)
    if _key in obj:
        return exists(obj[_key], chain) if chain else obj[_key]


def valid(message):
    '''
    Check if list of expected_key(nested and not nested) exists in `message` (dict)
    '''
    expected_keys = [['id_str'], ['user'], ['created_at'],['user', 'id_str'], ['user', 'created_at'], ['user', 'screen_name'], ['user', 'lang'],
    ['user', 'location'], ['user', 'followers_count'], ['user', 'friends_count'], ['user', 'statuses_count'],
    ['entities', 'urls'], ['entities', 'hashtags']]
    for expected_key in expected_keys:
        if not exists(message, expected_key):
            return False
    return True

#

def worker():
    '''
    Retrieve twitter from kafka "tweet" topic, and write to the database
    '''
    conn = DBConnect().getDB()
    while True:
        for message in consumer:
            try:
                if valid(message.value):
                    dbrt = DBWrite(conn)
                    print "writing twitter activity:" + message.value['id_str'] + " to database ..."
                    #parent 1: user_static: primary key; user_id
                    dbrt.write_user_static(message.value['user']['id_str'], message.value['user']['created_at'],
                        message.value['user']['screen_name'],message.value['user']['lang'],
                        message.value['user']['location'])

                    #parent2: twitteraw: primary key: activity_id
                    # use json.dumps to convert message.value to string
                    dbrt.write_raw(message.value['id_str'], json.dumps(message.value))


                    #use json.dumps to convert object to string
                    dbrt.write_activity(message.value['id_str'], message.value['created_at'], message.value['text'],
                        message.value['user']['id_str'],  json.dumps(message.value['entities']['urls']))
                    dbrt.write_user_dynamic(message.value['user']['id_str'], message.value['id_str'],
                        message.value['user']['followers_count'], message.value['user']['friends_count'], message.value['user']['statuses_count'])
                    #each twitter activity has multiple hashtag
                    dbrt.write_hashtags(message.value['id_str'], message.value['entities']['hashtags'])

            except Exception as e:
                print type(e), str(e)


if __name__ == '__main__':
    #for useing docker
    # consumer = KafkaConsumer('tweet', bootstrap_servers = ['kafka:9092'], value_deserializer = lambda m: json.loads(m.decode('utf-8')))
    #for using local machine
    consumer = KafkaConsumer('tweet', bootstrap_servers = ['localhost:9092'], value_deserializer = lambda m: json.loads(m.decode('utf-8')))
    worker()
