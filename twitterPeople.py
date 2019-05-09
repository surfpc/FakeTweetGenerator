# -*- coding: utf-8 -*-

import json
import tweepy


language = "en"

# Some sample id's 
#trump_id = 25073877
#elon_id = 44196397
#buzzfeed_id = 5695632
#showerthoughts_id = 487736815


tweetCount = 1000

# gets roughly 1000 tweets from the user associated with the given ID
def getTweets(id_num, consumerKey, consumerSecret, accessToken, accessSecret):
    #creating the authentication object
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    #setting your access token and secret
    auth.set_access_token(accessToken, accessSecret)
    #creating the API object while passing in auth information
    api = tweepy.API(auth)
    
    result = []
    for i in range(1, 100):
        for tweet in api.user_timeline(id=id_num, count=tweetCount, tweet_mode='extended', page=i):
            #print(tweet.retweeted)
            if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                sep = 'https'
                result.append({
                    'text': tweet.full_text.split(sep, 1)[0]
                })
        
    #dumps all the data into a JSON file
    with open('json/' + str(id_num) + '_tweets.json', 'w+') as f:
        json.dump(result, f)

