#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      07 June 2014

PROJECT:            Automatron
DESCRIPTION:        Returns and stores the twitter searches

#######################################################################################################
'''

import twitter
import logging
import string
from sqlalchemy import *

import WordLists as w
import Automatron_Reference as r
import Automatron_ReferencePrivate as rp


def tweet_contains_wordlist_term(words_in_tweet, wordlist):
    ''' Returns true or false depending on whether tweet contains any word from a given wordlist '''

    filter_text = list(set(words_in_tweet).intersection(set(wordlist)))

    return filter_text <> []
 

def tweet_contains_offensive_term(tweet_content):
    ''' Tests whether the tweet contains any offensive or banned terms '''

    FN_NAME = "tweet_contains_offensive_term"

    output = False

    list_of_wordlists = [
                        w.WORDLIST_BANNED_OFFENSIVE,
                        w.WORDLIST_BANNED_SLANG,
                        w.WORDLIST_BANNED_NEGATIVE,
                        w.WORDLIST_BANNED_AMERICANISMS,
                        w.WORDLIST_BANNED_EDUCATION,
                        w.WORDLIST_BANNED_FOOD,
                        w.WORDLIST_BANNED_GENDER
                        ]

    try:

        # Remove the punctuation from the string
        test_string = ''.join(ch for ch in tweet_content if ch not in set(string.punctuation))

        # Convert the text string to a standard format
        words_in_tweet = test_string.lower().split()

        for wordlist in list_of_wordlists:

            if tweet_contains_wordlist_term(words_in_tweet, wordlist):

                output = True
                break

    except Exception, e:
    
        logging.error('%s Unable to test for offensive term in tweet', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:

        return output


def tweet_contains_forbidden_characters(tweet_content):
    ''' Tests whether the tweet contains characters that will break the SQL '''

    FN_NAME = "tweet_contains_forbidden_characters"

    output = False

    test_string = tweet_content.lower()

    try:

        for word in w.WORDLIST_BANNED_STRINGSEARCH:

            if word in test_string:
                print word

                output = True
                break

    except Exception, e:
    
        logging.error('%s Unable to remove forbidden characters', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:

        return output


def percentage_of_capitals_in_string(input_string):
    ''' Calculates the percentage of letters in a string represented by capital letters '''

    output_percentage = (sum(x.isupper() for x in input_string)) / (max(len(input_string),1)*1.0)

    return output_percentage


def percentage_of_common_words(tweet_text):
    ''' Returns the percentage of words in the tweet that appear in the '1000 most common words' list '''

    FN_NAME = "percentage_of_common_words"

    output = 0.0
    
    try:
        tweet_list = tweet_text.lower().split()
            
        total_number_of_words = len(tweet_list) * 1.0 # Convert to long type
    
        words_in_frequency_list = len([word for word in tweet_list if word in w.WORDLIST_MOST_FREQUENT_1000])

        output = round(words_in_frequency_list / max(total_number_of_words,1),9)

    except Exception, e:
    
        logging.error('%s Unable to create a list of search results', FN_NAME)
        logging.exception('Traceback message: \n%s',e)
        
    finally:

        return output



def create_list_of_search_results(api, SearchTerm, LengthOfSearch=50):
    '''Searches Twitter for the terms passed in the list and returns a time-stamped list of the search terms and returned statuses'''

    FN_NAME = "create_list_of_search_results"
    
    results_list = []

    try:
        
        search_result = api.GetSearch(term=SearchTerm, count=LengthOfSearch)
        
        for s in search_result:

            # Convert to standard format - capitalise first letter etc
            tweet_text = standard_format_text_string((s.text).encode('utf-8'))

            if tweet_contains_offensive_term(tweet_text) == False:

                # Remove tweets with links or messages
                if tweet_contains_forbidden_characters(tweet_text) == False:

                    tweet_id = s.id

                    favourites_count = s.favorite_count

                    retweet_count = s.retweet_count

                    percentage_words = percentage_of_common_words(tweet_text)

                    tweeter_id = s.user.id
                    tweeter_followers = s.user.followers_count
                    tweeter_friends = s.user.friends_count
                    tweeter_status_count = s.user.statuses_count

                    follower_index = ((1.0*tweeter_followers)-tweeter_friends)/max(1,tweeter_friends)
            
                    results_list.append((tweet_id, tweet_text,retweet_count,favourites_count,len(tweet_text),percentage_words,tweeter_followers, tweeter_status_count, tweeter_id, tweeter_friends, follower_index))

    except Exception, e:
    
        logging.error('%s Unable to create a list of search results', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:
            
        return results_list



def filter_for_quality(tweet_metadata): ###rename function###
    ''' Filters the tweets for language quality so that only re-tweetable text strings populate the database '''

    output = False

    # Check that the tweet doesn't contain too many capital letters
    if percentage_of_capitals_in_string(tweet_metadata[1]) < r.SEARCHTEXT_MAX_CAPITALSPERCENT:

        # Ensure that the tweets aren't too short
        if tweet_metadata[4] > r.SEARCHTEXT_MIN_LENGTHOFTWEET:

            # Exclude tweets that don't contain sufficient number of 'real' words
            if tweet_metadata[5] > r.SEARCHTWEET_MIN_PERCENTAGEWORDS:

                # Exclude tweets where the original tweeter is too popular (helps mitigate detection risk)  
                if tweet_metadata[6] < r.SEARCHTWEET_MAX_FOLLOWERS:

                    # Exclude users with no friends (helps filter out spam accounts and bots)
                    if tweet_metadata[9] > r.SEARCHTEXT_MIN_FRIENDS:

                        # Exclude accounts that tweet too often, such as companies or bots
                        if tweet_metadata[7] < r.SEARCHTWEET_MAX_NUMBEROFTWEETS:

                            output =  True

    return output


def standard_format_text_string(input_string):
    ''' Converts the input text string into a standard format '''

    FN_NAME = "standard_format_text_string"

    output_string = ""
    input_string_list = []

    try:

        # Remove quotation marks from start and end of string
        if input_string[0] == '"' and input_string[-1] == '"':
            intput_string = input_string[1:-1]        
    
        # Make sure that the first letter is capitalised
        input_string = input_string[0].strip().upper() + input_string.strip()[1:]

        # Replaces any unicode characters (including emoticons) with a single space
        input_string = ''.join([i if ord(i) < 128 else ' ' for i in list(input_string)])

        # Remove any doublespaces in the sentence
        input_string_list = input_string.split()
        for i in range(0,len(input_string_list)):
            if i == len(input_string_list) - 1:
                output_string = output_string + input_string_list[i]
            else:        
                output_string = output_string + input_string_list[i] + " "

    except Exception, e:
    
        logging.error('%s Unable to create a list of search results', FN_NAME)
        logging.exception('Traceback message: \n%s',e)
    
    finally:

        return output_string


def search_twitter(SearchTerm):
    '''Scans Twitter for trending terms, searches for those terms and populates a database with the results'''
    
    FN_NAME = "search_twitter"
    
    process_result = False

    try:
    
        # Establish the api connection
        api = twitter.Api(
                      consumer_key = rp.CONS_AUTOMATRON_TOKEN,
                      consumer_secret = rp.CONS_AUTOMATRON_SECRET,
                      access_token_key = rp.ACCESS_AUTOMATRON_TOKEN,
                      access_token_secret = rp.ACCESS_AUTOMATRON_SECRET
                      )
    
        # Establish the connection to the database
        db = create_engine(rp.DB_CONNECTTION_STRING)
        metadata = MetaData(db)

        db.echo = False

        tweet_results = Table('tbl_DATA_SearchTweets', metadata, autoload = True)
        tweet_results_insert = tweet_results.insert()
                   
        # Return 100 most recent tweents for each trending item
        search_result_list =  create_list_of_search_results(api, SearchTerm, 100)
            
        if search_result_list: # Checks whether the list is empty
            
            # Insert into the database
            for tweet in search_result_list:

                if filter_for_quality(tweet): # Filters out words in non-English languages

                    # Check if tweet already in database

                    print tweet
            
                    tweet_results_insert.execute({
                                        'ID' : tweet[0],
                                        'TweetText' : tweet[1],
                                        'NumberOfRetweets' : tweet[2],
                                        'NumberOfFavourites' : tweet[3],
                                        'LengthOfTweet' : tweet[4],
                                        'PercentageWords' : tweet[5],
                                        'TweeterFollowers' : tweet[6],
                                        'TweeterStatusCount' : tweet[7],
                                        'UserID' : tweet[8],
                                        'TweeterFriends' : tweet[9],
                                        'FollowerIndex' : tweet[10]
                                        })
                
            process_result = True

    except Exception, e:
    
        logging.error('%s Unable to create a search list of tweets', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:

        return process_result

