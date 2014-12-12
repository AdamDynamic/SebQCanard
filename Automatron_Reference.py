#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      12 July 2014

PROJECT:            Automatron
DESCRIPTION:        Contains constants used to configure the modules

#######################################################################################################
'''

# Search Terms to populate the database
SEARCH_TERMS = ['moustache',
                'cigar',
                'straightblade',
                'haberdasher',
                'glenlivet',
                'bookshelf',
                'book',
                'backgammon',
                'chess',
                'puccini',
                'troubadour',
                'tobacconist']

SEARCHTWEET_MAXROWS = 1000          # Limits size of the tbl_DATA_SearchTweets table

SEARCHTWEET_MAXTERMS = 5            # The number of terms from SEARCH_TERMS that gets searched for each time

TWEETS_MAX_PER_DAY = 8              # Limits the total output of tweets per day

FOLLOWERS_MAX_PER_DAY = 5           # Limits the number of new followers made per day

FOLLOWERS_SEED_MAX_RATIO = 0.1      # Helps target users who follow back
FOLLOWERS_SEED_MAX_FRIENDS = 5000   # Prevents the seed user from having too many friends
FOLLOWERS_SEED_MIN_FRIENDS = 500    # Ensures the seed user has enough friends to make a following them useful

### Filter Criteria ###
# Sets the minimum standards for tweets to populate the database
SEARCHTWEET_MIN_PERCENTAGEWORDS = 0.2
SEARCHTWEET_MAX_FOLLOWERS = 1000            # Prevents tweets from popular users being re-tweeted
SEARCHTEXT_MIN_FRIENDS = 5                  # Helps filter out bot or spam accounts
SEARCHTWEET_MAX_NUMBEROFTWEETS = 50000      # Prevents tweets from popular users, organisations, automatic/bot accounts
SEARCHTEXT_MIN_LENGTHOFTWEET = 10
SEARCHTEXT_MAX_CAPITALSPERCENT = 0.1        # Filters tweets with all caps or 'shouting'

# The probability constants for time of the day that a tweet is made
HOURLY_PROFILE_2330_0730 = 0.0
HOURLY_PROFILE_0731_0900 = 0.02
HOURLY_PROFILE_0901_1200 = 0.02
HOURLY_PROFILE_1201_1400 = 0.04
HOURLY_PROFILE_1401_1600 = 0.04
HOURLY_PROFILE_1601_1800 = 0.04
HOURLY_PROFILE_1801_2000 = 0.02
HOURLY_PROFILE_2001_2200 = 0.02
HOURLY_PROFILE_2200_2329 = 0.02

# Define features of the host twitter account
TWITTER_USER_NAME = "SebQCanard"

# Define the names of table in the database
DB_TABLE_TEXTOUTPUT = "`tbl_DATA_TextOutput`"
DB_TABLE_FOLLOWERS = "`tbl_DATA_Followers`"
DB_TABLE_FOLLOWERS_REQUESTED = "`tbl_DATA_FollowerRequests`"
DB_TABLE_FOLLOWERNETWORK = "`tbl_DATA_FollowerNetwork`"
DB_TABLE_TWEETSMADE = "`tbl_DATA_TweetsMade`"
DB_TABLE_SEARCHTWEETS = "`tbl_DATA_SearchTweets`"

# Column names from the TextOutput table
FIELD_OUTPUT_TYPE = "`OutputType`"
FIELD_OUTPUT_CONTENT = "`OutputContent`"

# Column names from the Followers table
FIELD_FOLLOWERS_ID = "`ID`"
FIELD_FOLLOWERS_SCREENNAME = "`ScreenName`"
FIELD_FOLLOWERS_USERNAME = "`UserName`"
FIELD_FOLLOWERS_DATE = "`TimeStamp`"
FIELD_FOLLOWERS_CREATED = "`DateCreated`"
FIELD_FOLLOWERS_TYPE = "`Type`"
FIELD_FOLLOWERS_COUNT_STATUS = "`StatusCount`"
FIELD_FOLLOWERS_COUNT_FRIEND = "`FriendCount`"
FIELD_FOLLOWERS_COUNT_FOLLOWER = "`FollowerCount`"
FIELD_FOLLOWERS_COUNT_FAVOURITE = "`FavouriteCount`"

# Column names from the FollowerRequests table
FIELD_FOLLOWERS_REQ_DATE = "`TimeStamp`"
FIELD_FOLLOWERS_REQ_ID = "`ID`"
FIELD_FOLLOWERS_REQ_SCREENNAME = "`ScreenName`"
FIELD_FOLLOWERS_REQ_USERNAME = "`UserName`"
FIELD_FOLLOWERS_REQ_COUNT_STATUS = "`StatusCount`"
FIELD_FOLLOWERS_REQ_COUNT_FOLLOWER = "`FollowerCount`"
FIELD_FOLLOWERS_REQ_COUNT_FRIEND = "`FriendCount`"

# Column names from the FollowersNetwork table
FIELD_FOLLOW_NTWK_SOURCEID = "`SourceID`"
FIELD_FOLLOW_NTWK_SOURCESCREENNAME = "`SourceScreenName`"
FIELD_FOLLOW_NTWK_ID = "`TargetID`"
FIELD_FOLLOW_NTWK_CREATED = "`TargetCreated`"
FIELD_FOLLOW_NTWK_SCREENNAME = "`TargetScreenName`"
FIELD_FOLLOW_NTWK_COUNT_STATUS = "`TargetStatusCount`"
FIELD_FOLLOW_NTWK_COUNT_FRIEND = "`TargetFriendCount`"
FIELD_FOLLOW_NTWK_COUNT_FOLLOWER = "`TargetFollowerCount`"
FIELD_FOLLOW_NTWK_COUNT_FAVOURITE = "`TargetFavouriteCount`"

# Column names from the TweetsMade table
FIELD_TWEETS_DATETIME = "`DateTime`"
FIELD_TWEETS_CONTENT = "`Content`"
FIELD_TWEETS_TWEETID = "`TweetID`"
FIELD_TWEETS_USERID = "`UserID`"

# Column names for the SearchTweets table
FIELD_SEARCH_ID = "ID"
FIELD_SEARCH_TEXT = "TweetText"
FIELD_SEARCH_USERID = "`UserID`"
FIELD_SEARCH_RETWEETS = "NumberOfRetweets"
FIELD_SEARCH_FAVOURITES = "NumberOfFavourites"
FIELD_SEARCH_LENGTH = "LengthOfTweet"
FIELD_SEARCH_PERCENTAGE = "PercentageWords"
FIELD_SEARCH_COUNT_FOLLOWERS = "TweeterFollowers"
FIELD_SEARCH_COUNT_FRIENDS = "`TweeterFriends`"
FIELD_SEARCH_FOLLOWERINDEX = "`FollowerIndex`"
FIELD_SEARCH_COUNT_STATUSES = "TweeterStatusCount"



   


