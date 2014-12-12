#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      05 June 2014

PROJECT:            Automatron
DESCRIPTION:        Includes functions that perform maintenance on the database

#######################################################################################################
'''

import MySQLdb
import logging

import Automatron_Reference as r
import Automatron_ReferencePrivate as rp

def replace_table_with_query_results(table_name, replacement_query):
    ''' Replaces the contents of a table with the results of a query on the same table '''

    FN_NAME = "replace_table_with_query_results"

    try:

    # Establish the connection to the database
        db = MySQLdb.connect(
                     host=rp.DB_HOST,
                     user=rp.DB_USER,
                     passwd=rp.DB_PASSWORD,
                     db=rp.DB_NAME
                     )
        
        cur = db.cursor()

        # Seperate queries as MySQLdb doesn't allow multiple queries in the same input string
        query1 = "CREATE TEMPORARY TABLE temp_table LIKE " + table_name + "; "
        query2 = "INSERT INTO temp_table " + replacement_query
        query3 = "TRUNCATE TABLE " + table_name + "; "
        query4 = "INSERT INTO " + table_name + " SELECT * FROM temp_table; "
        query5 = "DROP TEMPORARY TABLE temp_table; "
        
        cur.execute(query1)
        cur.execute(query2)
        cur.execute(query3)
        cur.execute(query4)
        cur.execute(query5)
        
        db.commit()

    except Exception, e:
    
        logging.error('%s Unable to replace contents of table', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:
        db.close()


def remove_duplicates_from_table(table_name, column_with_duplicates):
    ''' Removes duplicates from the table using a given column to filter for unique values '''

    unique_values_query = "SELECT * FROM " + table_name + " GROUP BY " + column_with_duplicates+ "; "

    replace_table_with_query_results(table_name, unique_values_query)


def limit_searchtweet_to_1000_rows():
    ''' Ranks the SearchTweet database and truncates all but the first 1000 rows '''

    # Rank the tweets according to (in order) retweets, favourites, follower/following weighting:        
    # Weighting factor given as ((Number of people you follow - Number of people who follow you) / Number of people who follow you)
    # Designed to favour those with lots of followers but who don't automatically follow back (assumed to have better tweet content)
        
    truncate_query = "SELECT * FROM " + r.DB_TABLE_SEARCHTWEETS + " ORDER BY " + r.FIELD_SEARCH_RETWEETS + " DESC, " + r.FIELD_SEARCH_FAVOURITES + " DESC, ((" + r.FIELD_SEARCH_COUNT_FRIENDS + "-" + r.FIELD_SEARCH_COUNT_FOLLOWERS + ")/" + r.FIELD_SEARCH_COUNT_FRIENDS + ") DESC LIMIT " + str(r.SEARCHTWEET_MAXROWS) + ";"

    replace_table_with_query_results(r.DB_TABLE_SEARCHTWEETS, truncate_query)


def remove_tweets_already_tweeted():
    ''' Removes from the list any tweets that the bot has already copied and tweeted '''

    tweets_copied_query = "SELECT * FROM " + r.DB_TABLE_SEARCHTWEETS + " WHERE " + r.FIELD_SEARCH_TEXT + " NOT IN (SELECT " + r.FIELD_TWEETS_CONTENT + " FROM " + r.DB_TABLE_TWEETSMADE + ")"
    print tweets_copied_query
    replace_table_with_query_results(r.DB_TABLE_SEARCHTWEETS, tweets_copied_query)


def remove_tweets_from_friends():
    ''' Removes from the list of tweets any made by friends in the bot's network '''

    friends_tweets_query = "SELECT * FROM " + r.DB_TABLE_SEARCHTWEETS + " WHERE " + r.FIELD_SEARCH_USERID + " NOT IN (SELECT " + r.FIELD_FOLLOWERS_ID + " FROM " + r.DB_TABLE_FOLLOWERS + ")"

    replace_table_with_query_results(r.DB_TABLE_SEARCHTWEETS, friends_tweets_query)


def process_database_maintenance():
    ''' Runs all the required functions that maintain/clean/optimise/etc the databases used '''

    FN_NAME = "process_database_maintenance"

    result = False

    try:

        # Ensure that tweets only appear in the SearchTweets database once
        remove_duplicates_from_table(r.DB_TABLE_SEARCHTWEETS,r.FIELD_SEARCH_ID)

        # Truncate the SearchTweet database to 1000 rows
        limit_searchtweet_to_1000_rows()

        # Need to remove tweets that the bot has already made from the list
        remove_tweets_already_tweeted()

        # Remove tweets from users in the bot's network
        remove_tweets_from_friends()

        result = True

    except Exception, e:
    
        logging.error('%s Unable to process database maintenance', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:

        return result


