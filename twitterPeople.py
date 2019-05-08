# -*- coding: utf-8 -*-

import json
import tweepy

#consumerKey = "#"
#consumerSecret = "#"
#accessToken = "#-#"
#accessSecret = "#"

#creating the authentication object
#auth = tweepy.OAuthHandler(consumerKey, consumerSecret)

#setting your access token and secret
#auth.set_access_token(accessToken, accessSecret)

#creating the API object while passing in auth information
#api = tweepy.API(auth)


language = "en"
#results = api.search(q=query, lang=language, rpp=100) #get most recent tweets

#results = [] #api.user_timeline(user_id=25073877, count=1000)

trump_name = 25073877
elon_name = 44196397
buzz_name = 5695632
shower_name = 487736815
tweetCount = 1000

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
        
    with open('json/' + str(id_num) + '_tweets.json', 'w+') as f:
        json.dump(result, f)

#for tweet in results:
#    print(tweet.text)
