# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# lots of Twitter Python libraries: [Twitter Libraries | Twitter Developers](https://dev.twitter.com/docs/twitter-libraries#python)
# 
# I have a little bit of experience with [tweepy/tweepy](https://github.com/tweepy/tweepy).
# 
# easiest way to install is
# 
#     pip install tweepy
#     

# <markdowncell>

# create a new app: https://apps.twitter.com/app/new to get token.
#         
# Set the appropriate permission level

# <codecell>

import os
import sys
import pickle
import tweepy

from settings import (TWITTER_CONSUMER_KEY,
                      TWITTER_CONSUMER_SECRET,
                      TWITTER_ACCESS_TOKEN, 
                      TWITTER_ACCESS_TOKEN_SECRET)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame

TWITTER_HANDLE = 'rdhyee'

# <codecell>

# http://tweepy.readthedocs.org/en/v2.3.0/getting_started.html

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text

# <codecell>

# a "hello world" identity decorator, written to get a handle on the concept.

def identity(func):
    def newf(*args, **kwargs):
        return func(*args, **kwargs)
    return newf

# this decorator is used to handle those tweepy calls whose results can be paged via a cursor.
# http://pythonhosted.org/tweepy/html/cursor_tutorial.html

def cursorize(func):
    def newf(*args, **kwargs):
        for item in tweepy.Cursor(func, *args, **kwargs).items():
            yield item

    return newf

# <codecell>

from itertools import islice

follower_ids = list(cursorize(api.followers_ids)(screen_name=TWITTER_HANDLE))
friend_ids = list(cursorize(api.friends_ids)(screen_name=TWITTER_HANDLE))

# <codecell>

follower_ids

# <codecell>

api.update_status("hello using tweepy")

