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
from sqlalchemy import *

import Automatron_Reference as r
import WordLists as w


# Establish the connection to the database
db = MySQLdb.connect(
                     host=r.DB_HOST,
                     user=r.DB_USER,
                     passwd=r.DB_PASSWORD,
                     db=r.DB_NAME
                     )
        
cur = db.cursor()

# Establish the Twitter api connection
api = twitter.Api(
                  consumer_key = r.CONS_AUTOMATRON_TOKEN,
                  consumer_secret = r.CONS_AUTOMATRON_SECRET,
                  access_token_key = r.ACCESS_AUTOMATRON_TOKEN,
                  access_token_secret = r.ACCESS_AUTOMATRON_SECRET
                  )


class CurrentFollowers(object):
    ''' Class to deal with followers of the Twitter account'''

    def GetTwitterFollowers(self):
        ''' Get the list of followers from Twitter '''
        AllTwitterFollowers = api.GetFollowers()

        self.followers = AllTwitterFollowers
        

    def AreNew(self):
        ''' Returns a list of all users that are new followers '''

        # Get the list of current followers from the database by their id
        Query = "SELECT " + r.FIELD_FOLLOWERS_ID + " FROM " + r.DB_TABLE_FOLLOWERS + ";"
        cur.execute(Query)
        AllUsersDatabase = [item[0] for item in cur.fetchall()]

        NewFollowers = [item for item in self.followers if item.id not in AllUsersDatabase]

        return NewFollowers

    def Unfollow(self):
        ''' Unfollow those users who haven't followed back within a week '''

        pass


class NewFollower(object):
    ''' Class to deal with followers identified as 'new' '''

    def _SetDetails(self,details): ### Do as __init__ ? ###
        ''' Set the twitter api results of the new follower '''
        self.details = details

    def _AddToDatabase(self):
        ''' Adds the details of the new follower to the database '''

        FollowerType = "Real" # Used to distinguish new followers from purchased bot followers
        FollowerScreenName = self.details.screen_name
        FollowerUserName = self.details.name
        FollowerID = str(self.details.id)
        FollowerCount_Status = str(self.details.statuses_count)
        FollowerCount_Friends = str(self.details.friends_count)
        FollowerCount_Followers = str(self.details.followers_count)
        FollowerCount_Favourite = str(self.details.favourites_count)
        FollowerDateCreated = datetime.datetime.strptime(self.details.created_at,'%a %b %d %H:%M:%S +0000 %Y')
        
        # Create timestamp
        ts = time.time()
        TimeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        # Add the details to the database
        Query = "INSERT INTO " + r.DB_TABLE_FOLLOWERS + "( " \
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

        cur.execute(Query)
        db.commit()
        
        return True

    def _FollowBack(self):
        ''' Automatically follows users who have followed the account providing they are 'real' '''

        #api.CreateFriendship(user_id = self.details.id)
        
        return True

    def _GetFollowersOfUser(self):
        ''' Determines the followers of new users so that user triangulation can be used to make new follower requests '''

        # Return all the users who follow the new user
        FollowersOfUser = api.GetFollowers(user_id = self.details.id) 

        # Populate these details into the database
        Details = [(item.id,
                    item.screen_name,
                    item.statuses_count,
                    item.friends_count,
                    item.followers_count,
                    item.favourites_count,
                    datetime.datetime.strptime(item.created_at,'%a %b %d %H:%M:%S +0000 %Y')
                    ) for item in FollowersOfUser]

        for item in Details:

            Query = "INSERT INTO " + r.DB_TABLE_FOLLOWERNETWORK + "(" \
                + r.FIELD_FOLLOW_NTWK_SOURCEID + ", " \
                + r.FIELD_FOLLOW_NTWK_SOURCESCREENNAME + ", " \
                + r.FIELD_FOLLOW_NTWK_ID + ", " \
                + r.FIELD_FOLLOW_NTWK_SCREENNAME + ", " \
                + r.FIELD_FOLLOW_NTWK_COUNT_STATUS + ", " \
                + r.FIELD_FOLLOW_NTWK_COUNT_FRIEND + ", " \
                + r.FIELD_FOLLOW_NTWK_COUNT_FOLLOWER + ", " \
                + r.FIELD_FOLLOW_NTWK_COUNT_FAVOURITE + ", " \
                + r.FIELD_FOLLOW_NTWK_CREATED + ") \
                VALUES ('" \
                + str(self.details.id) + "', '" \
                + self.details.screen_name + "', '" \
                + str(item[0]) + "', '" \
                + str(item[1]) + "', '" \
                + str(item[2]) + "', '" \
                + str(item[3]) + "', '" \
                + str(item[4]) + "', '" \
                + str(item[5]) + "', '" \
                + str(item[6]) + "');"

            cur.execute(Query)
            
        db.commit()
        
        return True

    def _Greet(self):
        ''' Sends a random greeting to new followers to thank them for following '''

        # Select a random user greeting from the database
        Query = "SELECT " + r.FIELD_OUTPUT_CONTENT + " FROM " + r.DB_TABLE_TEXTOUTPUT + " WHERE " + r.FIELD_OUTPUT_TYPE + " = 'NewFollower' ORDER BY RAND() LIMIT 1"

        cur.execute(Query)

        Message = cur.fetchall()[0][0]
        Message = Message[:140] # Truncate the message to the allowable number of characters
        
        print Message

        #api.PostDirectMessage(Message,self.details.id)

        return True

    def _UserAlreadyAFollower(self):
        ''' Determines whether the user is already in the follower database '''

        Query = "SELECT " + FIELD_FOLLOWERS_ID + " FROM " + r.DB_TABLE_FOLLOWERS + " WHERE " + FIELD_FOLLOWERS_ID + " = '" + str(self.details.id) + "';"
        cur.execute(Query)
        Output = cur.fetchall()

        return Output != ()

    def Create(self, details):
        ''' Runs all methods require to populate all database tables for a new follower '''
        
        self._SetDetails(details)

        if _UserAlreadyAFollower == False:
            
            self._AddToDatabase()
            self._GetFollowersOfUser()
            self._Greet()
            self._FollowBack()
            
        else:
            print self.screen_name + ": User already being followed, details in database"

class NewFriends(object):
    ''' Handles the process whereby new friends are added '''

    def Create(self):

        pass






logging.basicConfig(filename='Automatron_LogFile.log', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.ERROR)





NewTweet = CreateTweet()
NewTweet.content = "Hello, this is my content"
NewTweet.StoreTweetInDatabase()


# Search for tweets
 # Remove:
 # Anything with '@' sign
 # Anything with a link
 # Anything with a swear word
 # Anything with gender

# Store in database all returned tweets
# Flag those that have been favourited or retweeted

# When prompted by cron, test probability
# If passed, choose a random tweet based on the tweets available and tweet




'''

### Main ###

try:

    Followers = CurrentFollowers()

    # Determine which of the current Twitter followers have not already been captured by the 'new follower' process
    Followers.GetTwitterFollowers()
    NewFollowers = Followers.AreNew()

    # If any of the users are new, register their details in the database
    if NewFollowers:
        
        for  User in NewFollowers:

            print User

            NewFollowerEntry = NewFollower()
            NewFollowerEntry.Create(User)
            
finally:
    
    db.close()

'''





# Determine profile of the Automatron:
    # Male
    # Interested in tech / design / coding
    # Based in London
    # Follows trends and posts relevant information to followers
    

# Import data
    # Possible sources;
        # blogs (rss?)
        # popular twitter users
        # news articles
        # google search trends
        # what key people have liked on facebook?

    # Need a way of ranking data for importance / determining if it's relevant
    # Create list of keywords and scan for content?
    # Generate the list of keywords dynamically? i.e. 'interests' evolves over time


# Calculate
 # IFTTT approach?
 # Need to be able to construct simple sentences based on input
 # Simple statement then link to content? "Really excited about this bit.ly/fdjsf"
 
# Pre-set lists of questions/quotes/comments?

# Take tweets from other people and post them as it's own? (search for relevant keywords)


# Time to tweet depends on time of the day (profile based on work/sleep patterns)



# Retweet trending topics that fall within the interest range


# Refollow any new followers
    # Need to determine the list of current followers
    # Create list of messages used to greet new refollows

    # Consider 'triangulation' - making the social graph look authentic

    # Follow new users but unfollow anyone who doesn't follow back within 24 hours (maintain a sensible ratio)

    # Implement a simple algorithm for determining who is a bot (don't follow)



# Set up IFTTT.com page to post on facebook anything that's tweeted
