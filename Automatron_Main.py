#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      27 June 2014

PROJECT:            Automatron
DESCRIPTION:        Main routine

#######################################################################################################
'''

import logging
import random

from Automatron_TwitterSearch import search_twitter
from Automatron_DatabaseMaintenance import process_database_maintenance
from Automatron_TweetOutput import AutoTweet
from Automatron_Followers import new_follower

import Automatron_Reference as r

logging.basicConfig(filename='Automatron_LogFile.log', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# Create random sublist of searchterms (to mitigate risk of exceeding hourly connection limit)
random_sub_searchlist = random.sample(r.SEARCH_TERMS, r.SEARCHTWEET_MAXTERMS)

search_string = ""

# Create searchlist string to search for multiple terms at once
for search_term in random_sub_searchlist:
    search_string = search_string + search_term + " OR "

#search_twitter(search_string)

# Cleanse the database, remove duplicates etc
process_database_maintenance()

# Output a tweet
new_tweet = AutoTweet()
new_tweet.create_tweet()

# Add a new friend
new_follower = new_follower()
new_follower.create()




