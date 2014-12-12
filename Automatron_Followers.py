#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      08 March 2014

PROJECT:            Automatron
DESCRIPTION:        Governs the behaviour for following other users

#######################################################################################################
'''

import twitter
import MySQLdb
import time
import datetime
import logging
import random

import Automatron_Reference as r
import Automatron_ReferencePrivate as rp


class new_follower(object):
    ''' Class to deal with followers identified as "new" '''

    def __init__(self):
        ''' Set the twitter api results of the new follower '''
        
        self.id = 0

    def select_random_user(self):
        ''' Selects a random user from the database of search tweets '''

        FN_NAME = "select_random_user"
        
        # Establish the connection to the database
        db = MySQLdb.connect(
                     host=rp.DB_HOST,
                     user=rp.DB_USER,
                     passwd=rp.DB_PASSWORD,
                     db=rp.DB_NAME
                     )
        
        cur = db.cursor()

        try:

            query = "SELECT " + r.FIELD_SEARCH_USERID + " FROM " + r.DB_TABLE_SEARCHTWEETS + " WHERE " \
                + r.FIELD_SEARCH_COUNT_FRIENDS + " > " + str(r.FOLLOWERS_SEED_MIN_FRIENDS) + " AND " \
                + r.FIELD_SEARCH_COUNT_FRIENDS + " < " + str(r.FOLLOWERS_SEED_MAX_FRIENDS) + " AND " + \
                r.FIELD_SEARCH_FOLLOWERINDEX + " < " + str(r.FOLLOWERS_SEED_MAX_RATIO) + \
                " ORDER BY " + r.FIELD_SEARCH_FOLLOWERINDEX + " DESC LIMIT 1"

            cur.execute(query)

            self.id = cur.fetchall()[0][0]

        except Exception, e:

            logging.error('%s Unable to select random user', FN_NAME)
            logging.exception('Traceback message: \n%s',e)
            self.seed_user_id = 0

        finally:

            db.close()

    def get_user_details(self):
        ''' Gets the user details for the selected user from twitter '''

        FN_NAME = "get_user_details"

        # Establish the Twitter api connection
        api = twitter.Api(
                  consumer_key = rp.CONS_AUTOMATRON_TOKEN,
                  consumer_secret = rp.CONS_AUTOMATRON_SECRET,
                  access_token_key = rp.ACCESS_AUTOMATRON_TOKEN,
                  access_token_secret = rp.ACCESS_AUTOMATRON_SECRET
                  )

        try:

            random_user = api.GetUser(user_id = self.id)
            print random_user

            # Store details of random user
            self.screen_name = random_user.screen_name
            self.name = random_user.name
            self.id = random_user.id
            self.statuses_count = random_user.statuses_count
            self.friends_count = random_user.friends_count
            self.followers_count = random_user.followers_count
            self.favourites_count = random_user.favourites_count
            self.created_at = datetime.datetime.strptime(random_user.created_at,'%a %b %d %H:%M:%S +0000 %Y')

        except Exception, e:

            logging.error('%s Unable to get user details', FN_NAME)
            logging.exception('Traceback message: \n%s',e)
        
    def add_to_database(self):
        ''' Adds the details of the new follower to the database '''

        FN_NAME = "add_to_database"

        # Establish the connection to the database
        db = MySQLdb.connect(
                     host=rp.DB_HOST,
                     user=rp.DB_USER,
                     passwd=rp.DB_PASSWORD,
                     db=rp.DB_NAME
                     )
        
        cur = db.cursor()

        try:

            FollowerType = "Real" # Used to distinguish new followers from purchased bot followers
            FollowerScreenName = ''.join([i if ord(i) < 128 else ' ' for i in list(self.screen_name)])
            FollowerUserName = ''.join([i if ord(i) < 128 else ' ' for i in list(self.name)])
            FollowerID = str(self.id)
            FollowerCount_Status = str(self.statuses_count)
            FollowerCount_Friends = str(self.friends_count)
            FollowerCount_Followers = str(self.followers_count)
            FollowerCount_Favourite = str(self.favourites_count)
            FollowerDateCreated = self.created_at
            
            # Create timestamp
            ts = time.time()
            TimeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            # Add the details to the database
            query = "INSERT INTO " + r.DB_TABLE_FOLLOWERS + "( " \
                + r.FIELD_FOLLOWERS_ID + ", " \
                + r.FIELD_FOLLOWERS_SCREENNAME + ", " \
                + r.FIELD_FOLLOWERS_USERNAME + ", " \
                + r.FIELD_FOLLOWERS_DATE + ", " \
                + r.FIELD_FOLLOWERS_CREATED + ", " \
                + r.FIELD_FOLLOWERS_COUNT_STATUS + ", " \
                + r.FIELD_FOLLOWERS_COUNT_FRIEND + ", " \
                + r.FIELD_FOLLOWERS_COUNT_FOLLOWER + ", " \
                + r.FIELD_FOLLOWERS_COUNT_FAVOURITE + ", " \
                + r.FIELD_FOLLOWERS_TYPE + ") \
                VALUES ('" \
                + FollowerID + "', '" \
                + FollowerScreenName + "', '"  \
                + FollowerUserName + "', '" \
                + str(TimeStamp) + "', '" \
                + str(FollowerDateCreated) + "', '" \
                + str(FollowerCount_Status) + "', '" \
                + str(FollowerCount_Friends) + "', '" \
                + str(FollowerCount_Followers) + "', '" \
                + str(FollowerCount_Favourite) + "', '" \
                + FollowerType + "');"

            print query

            cur.execute(query)
            db.commit()

        except Exception, e:

            logging.error('%s Unable to add user to the database', FN_NAME)
            logging.exception('Traceback message: \n%s',e)

        finally:

            db.close()

    def follow_user_on_twitter(self):
        ''' Follows the randomly selected user on twitter '''

        FN_NAME = "follow_user_on_twitter"

        # Establish the Twitter api connection
        api = twitter.Api(
                  consumer_key = rp.CONS_AUTOMATRON_TOKEN,
                  consumer_secret = rp.CONS_AUTOMATRON_SECRET,
                  access_token_key = rp.ACCESS_AUTOMATRON_TOKEN,
                  access_token_secret = rp.ACCESS_AUTOMATRON_SECRET
                  )

        try:

            api.CreateFriendship(user_id = self.id)
        
        except Exception, e:

            logging.error('%s Unable to add user on twitter', FN_NAME)
            logging.exception('Traceback message: \n%s',e)

    def time_profile_probability(self):
        '''
        Determines the probability of making a tweet based on the time of the day

        Assumes that no tweets take place during the night (11.30pm to 7am)
        Tweets are less likely through the working day and more likely in the evening

        '''

        FN_NAME = "TimeProfileProbability"

        output_probability = 0.0
        
        try:
            
            current_time = datetime.datetime.now().time()

            # Test each timeslot through the day and return the relevant probability
            if current_time > datetime.time(23,30,0) and current_time <= datetime.time(23,59,59):

                output_probability = r.HOURLY_PROFILE_2330_0730

            elif current_time > datetime.time(0,0,0) and current_time <= datetime.time(7,30,0):

                output_probability = r.HOURLY_PROFILE_2330_0730

            elif current_time > datetime.time(7,30,0) and current_time <= datetime.time(9,0,0):

                output_probability = r.HOURLY_PROFILE_0731_0900

            elif current_time > datetime.time(9,0,0) and current_time <= datetime.time(12,0,0):

                output_probability = r.HOURLY_PROFILE_0901_1200

            elif current_time > datetime.time(12,0,0) and current_time <= datetime.time(14,0,0):

                output_probability = r.HOURLY_PROFILE_1201_1400

            elif current_time > datetime.time(14,0,0) and current_time <= datetime.time(16,0,0):

                output_probability = r.HOURLY_PROFILE_1401_1600

            elif current_time > datetime.time(16,0,0) and current_time <= datetime.time(18,0,0):

                output_probability = r.HOURLY_PROFILE_1601_1800

            elif current_time > datetime.time(18,0,0) and current_time <= datetime.time(20,0,0):

                output_probability = r.HOURLY_PROFILE_1801_2000

            elif current_time > datetime.time(20,0,0) and current_time <= datetime.time(22,0,0):

                output_probability = r.HOURLY_PROFILE_2001_2200

            elif current_time > datetime.time(22,0,0) and current_time <= datetime.time(23,30,0):

                output_probability = r.HOURLY_PROFILE_2200_2329

            else:

                pass

        except Exception, e:
    
            logging.error('%s Unable to store tweet in database', FN_NAME)
            logging.exception('Traceback message: \n%s',e)

        finally:

            return output_probability

    def number_of_friends_today(self):
        ''' Determines the number of friends made in the current day '''

        FN_NAME = "number_of_friends_today"

        try:

            # Establish the connection to the database
            db = MySQLdb.connect(
                                 host=rp.DB_HOST,
                                 user=rp.DB_USER,
                                 passwd=rp.DB_PASSWORD,
                                 db=rp.DB_NAME
                     )

            cur = db.cursor()
            
            # Return all tweets that haven't already been tweeted
            query = "SELECT COUNT(*) FROM " + r.DB_TABLE_FOLLOWERS + " WHERE " + r.FIELD_FOLLOWERS_DATE + " > CURDATE() - INTERVAL 1 DAY"
            print query

            cur.execute(query)
            number_of_friends = cur.fetchone()[0]
            
        except Exception, e:
    
            logging.error('%s Unable to determine the number of tweets in the day', FN_NAME)
            logging.exception('Traceback message: \n%s',e)
            

        finally:

            db.close()
            return number_of_friends

    def create(self):
        ''' Adds a new user based on a randomly selected user from the SearchTweet database '''

        FN_NAME = "create"

        try:

            # Test to see if the probability test is passed given the time of day
            hourly_profile = self.time_profile_probability()
            random_hourly_profile_test = random.random()

            if random_hourly_profile_test < hourly_profile:

                number_of_friends_created = self.number_of_friends_today()

                # Limit the number of friends made in a day to prevent malfunction
                if number_of_friends_created < r.FOLLOWERS_MAX_PER_DAY:

                    self.select_random_user()
                    print self.id

                    if self.id <> 0:

                        self.get_user_details()
                        self.follow_user_on_twitter()
                        self.add_to_database()

                        logging.info('%s Friend added: ' + self.screen_name, FN_NAME)

            else:

                # Don't make a tweet
                logging.info('%s Friend not added as hourly profile test not passed', FN_NAME)



        except Exception, e:
    
            logging.error('%s Unable to create new twitter friendship', FN_NAME)
            logging.exception('Traceback message: \n%s',e)



