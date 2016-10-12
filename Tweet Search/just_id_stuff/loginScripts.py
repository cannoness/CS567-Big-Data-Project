from just_id_streamer import JustIdStreamer
#from MyStreamer import MyStreamer
from twython import Twython
import sys
import json

#
# This is a file containing login scripts for twitter.
# Use streamLogin to use TwythonStreamer.
# Use searchLogin to perform a search.
#
# Justin Thomas
# 10/05/2016
#

# Modified to use just_id_streamer instead of MyStreamer.
# Vanessa Job
# October 7, 2106

CONSUMER_KEY = 'consumerKey'
CONSUMER_SECRET = 'consumerSecret'
ACCESS_TOKEN = 'accessToken'

def streamLogin(KEY_FILE_NAME):
    """
    Login to twitter, authorize and return MyStreamer, twitter streaming object.
    @param KEY_FILE_NAME String: Name of file containing the consumer key and secret.
    @return MyStreamer object, extends TwythonStreamer
    """

    keyFile = json.load(open(KEY_FILE_NAME))
    #read consumer key, strip trailing whitespace.
    APP_KEY = keyFile[CONSUMER_KEY]
    #read consumer secret, strip trailing whitespace.
    APP_SECRET = keyFile[CONSUMER_SECRET]
    #create Twython instance to get oauth tokens.
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_SECRET = auth['oauth_token_secret']

    #print url to get verification PIN.
    #prompt user to go to url and get PIN entry.
    print "\n\n\nGo to the following url and enter the PIN you find there."
    print auth['auth_url']
    verifier = raw_input()
    #get final OAUTH token and secret.
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
    finalStep = twitter.get_authorized_tokens(verifier)
    OAUTH_TOKEN = finalStep['oauth_token']
    OAUTH_SECRET = finalStep['oauth_token_secret']

    #return MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
    return JustIdStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)


def searchLogin(KEY_FILE_NAME):
    """
    Return a Twython object to perform a search.
    @param KEY_FILE_NAME String: name of the file with the keys.
    @return Twython object.
    """
    keyFile = json.load(open(KEY_FILE_NAME))
    return Twython(keyFile[CONSUMER_KEY], access_token=keyFile[ACCESS_TOKEN])
