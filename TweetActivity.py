# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 20:07:49 2019

@author: KhubaibAhmed
"""
import numpy as np
import time
import datetime
import tweepy
import pandas as pd
from matplotlib import pyplot as plt

MaxTweets =4000
userId=''
filename =userId+'.csv';   

# Consumer keys and access tokens, used for OAuth
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Creation of the actual interface, using authentication
api = tweepy.API(auth)


cols=['created_at','Hr','screen_name','id_str','text','id_str','favorite_count','retweet_count']
dfsts = pd.DataFrame(columns=cols)


tt=0;
c=tweepy.Cursor(api.user_timeline, screen_name=userId, exclude_replies = True).items(MaxTweets)
while True:
    try:
        tt=tt+1
        tweet = c.next()
        twit=tweet._json
        #Write a row to the csv file/ I use encode utf-8
        dfsts = dfsts.append(pd.Series([twit['created_at'],twit['created_at'][11:13], twit['user']['screen_name'],twit['user']['id_str'],twit['text'],twit['id_str'],twit['favorite_count'],twit['retweet_count']], index=cols), ignore_index=True)
    #        csvWriter.writerow([twit['created_at'], twit['user']['screen_name'],twit['user']['id_str'],twit['text'],twit['id_str'],twit['favorite_count'],twit['retweet_count']])
        print(tt,' - ',twit['user']['screen_name'],' - ',twit['created_at'][11:13])
        #, twit['user']['screen_name'],twit['user']['id_str'],twit['text'],twit['id_str'],twit['favorite_count'],twit['retweet_count']])
#        print("____________________________________________")
    except tweepy.TweepError:
        time.sleep(60 * 15)
        print(tt,'   ',datetime.datetime.now())
        continue
    except StopIteration:
        break        
Hrs=list(dfsts['Hr'])
Hrs = list(map(int, Hrs))
bins = np.arange(0, 24)
plt.xlim([0, 23])

plt.hist(Hrs, bins=bins, alpha=0.5,edgecolor='black', linewidth=1.2)
title="Activity of "+userId+"Considering last "+str(tt)+" tweets"
plt.title(title)
plt.xlabel('Hour 00 -> 23')
plt.ylabel('Number of Tweets')
plt.grid(True)
plt.show()
#dfsts.to_csv(filename, sep=',', encoding='utf-8')
