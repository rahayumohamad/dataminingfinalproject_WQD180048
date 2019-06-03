############################################################################################
#                                                                                          #
#      This code is written during team meet-up by team members as shown below ...         #
#                                                                                          #  
#                    HAFIFI BIN YAHYA - WQD170042                                          #
#                    NOR ASMIDAH BINTI MOHD ARSHAD - WQD180006                             #
#                    MAS RAHAYU BINTI MOHAMAD - WQD180048                                  #
#                    LEE CHUN MUN - WQD180066                                              #
#                    JOJIE ANAK NANJU - WQD180029                                          #
#                                                                                          #
############################################################################################

from __future__ import print_function
import tweepy
import json
#import MySQLdb
#import mysqlclient
#from dateutil import parser
from dateutil.parser import *
import pymysql

#WORDS = ['#bigdata', '#AI', '#datascience', '#machinelearning', '#ml', '#iot']
#WORDS = ['#news', '#BursaMalaysia', '#stocknews','#KLCI', '#BursaMalaysia', '#openingbell']
WORDS = ['#BursaMalaysia', '#stocknews','#KLCI', '#openingbell', '#stockinvestment', '#klsemarket', '#BursaMalaysiaTradeStatistics', '#1mdb', '#stockexchange',
         '#Bursa', '#Market', '#Index', '#stock', '#stocknews', '#KLSEtraders', '#KLSEnews', '#updates','#klsetraders']
#IWD2019

#CONSUMER_KEY = "KEY"
#CONSUMER_SECRET = "SECRET"
#ACCESS_TOKEN = "TOKEN"
#ACCESS_TOKEN_SECRET = "TOKEN_SECRET"

ACCESS_TOKEN = "69793210-cQfMYtjTriuL2dB0nCzftkTjYBsSB0z8YM4MWKo6n"
ACCESS_TOKEN_SECRET = "EtGiwIWFkYkFwCxUyvW3qOkbylgb4ONy5Np9MRTAEJQv2"
CONSUMER_KEY = "DSTr85cSnpFSELigMDsPoKGYI"
CONSUMER_SECRET = "ke9a5eXnRrVfNbeKU36UyRJegdIgi3QhUrBIsMC5OYBUlodm0X"

HOST = "localhost"
USER = "root"
PASSWD = ""
DATABASE = "KLSE"


# This function takes the 'created_at', 'text', 'screen_name' and 'tweet_id' and stores it
# into a MySQL database
def store_data(created_at, text, screen_name, tweet_id):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8")
    cursor = db.cursor()
    insert_query = "INSERT INTO twitter (tweet_id, screen_name, created_at, text) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (tweet_id, screen_name, created_at, text))
    db.commit()
    cursor.close()
    db.close()
    return


class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # grab the wanted data from the Tweet
            text = datajson['text']
            screen_name = datajson['user']['screen_name']
            tweet_id = datajson['id']
            created_at = parse(datajson['created_at'])

            # print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))

            # insert the data into the MySQL database
            store_data(created_at, text, screen_name, tweet_id)

        except Exception as e:
            print(e)


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)