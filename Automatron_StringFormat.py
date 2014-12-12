#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      08 June 2014

PROJECT:            Automatron
DESCRIPTION:        Formats the text string to create a standard output format for the bot

#######################################################################################################
'''

import string

import WordLists as w
import Automatron_Reference as r

list_of_punctuation = list(set(string.punctuation))


def space_string_correctly(input_string):
    ''' Ensures that the string has the correct number of spaces '''

    input_string_list = input_string.split()
    output_string = ""
    
    for i in range(0,len(input_string_list)):

        # Prevents a space being added to the end of the string
        if i == 0:            
            output_string = output_string + input_string_list[i]
            
        else:

            # Ensure spaces before punctuation are removed
            if input_string_list[i] in list_of_punctuation:
                output_string = output_string + input_string_list[i]

            else:
                output_string = output_string + " " + input_string_list[i]

    return output_string

def add_fullstop(input_string):
    ''' Adds a full stop if the string does not end with any other punctuation '''

    output_string = ""
    
    if input_string[-1] in list_of_punctuation:
        output_string = input_string[:]

    else:

        # Don't take the total string length above the length allowed for a tweet
        if len(input_string) < 140:
            output_string = input_string[:] + "."

    return output_string


def remove_emoticons(input_string):
    ''' removes any unicode in the input string '''

    output_string = ''.join([i if ord(i) < 128 else ' ' for i in list(input_string)])

    return output_string

def replace_punctuation_with_space(input_string):

    input_string_list = list(input_string)
    output_list = []

    for i in input_string_list:

        if i not in list(set(string.punctuation)):
            output_list.append(i)

        else:
            output_list.append(" ")

    output_string = ''.join(output_list)

    return output_string
        
            

def StandardFormatTextString(input_string):
    ''' Converts the input text string into a standard format '''

    FN_NAME = "StandardFormatTextString"

    output_string = ""
    input_string_list = []

    try:

        # Remove quotation marks from start and end of string
        if a[0] == '"' and a[-1] == '"':
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

test = "   this is the , the  thing?   "
test2 = "10 retweets and I'll shave my stache into a Hitler/Chaplin moustache"
print space_string_correctly(test)

print replace_punctuation_with_space(test2)
