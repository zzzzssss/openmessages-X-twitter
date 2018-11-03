import json
import tweepy
from kafka import KafkaProducer
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.config import Config

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(tweepy.StreamListener, self).__init__()
        self.num_tweets = 0

    def on_status(self, status):
        print status

    def on_data(self, data):
        # streaming data reference: https://dev.twitter.com/overview/api/tweets
        try:
             # Twitter returns data in JSON format - we need to decode it first
             self.num_tweets += 1
             if self.num_tweets < 1500:
                decoded = json.loads(data)
                if decoded.get('lang') =='en':
                    # pretty print json object
                    print json.dumps(decoded, sort_keys=True, indent=4, separators=(',', ': '))
                    producer.send('tweet', value = decoded)
                    return True
             else:
                return False
        except Exception as e:
            print type(e), str(e)
            return False

    def on_error(self, status):
        if status == 420:
            return False


if __name__ == '__main__':
    # start kafka and create topic tweet
    # Create Kafka Producer client
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    # read parameters that contains the user credentials to access Twitter API
    params = Config('config.ini', 'tweepyapi').getConfig()

    # get filter words from the command line
    filterword = []
    for i in range(len(sys.argv)):
        if i == 0:
            continue
        filterword.append(sys.argv[i])
    print filterword


    #start streaming with twweepy API
    ls = MyStreamListener()
    auth = tweepy.OAuthHandler(params['consumer_key'], params['consumer_secret'])
    auth.set_access_token(params['access_token'], params['access_token_secret'])
    stream = tweepy.Stream(auth, ls)
    stream.filter(track = filterword)



