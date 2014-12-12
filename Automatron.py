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
import Automatron_Reference as r

class NewFollower:

    def Greet(self):
        print "Hello, New Follower!"


Adam = NewFollower()

Adam.Greet()



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
