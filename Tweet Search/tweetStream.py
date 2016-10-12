from MyStreamer import MyStreamer
from twython import Twython
from collections import deque
import loginScripts
import sys
import json

#
# Driver to hook up to python stream.
# currently collecting tweets around NYC
# TODO Take args and collect tweets around various areas
#

KEY_FILE_NAME = 'keys1.json'
#string creating bounding box around NYC
LOC_NYC = '-74,40,-73,41'

def processTweets(tweetQueue):
    """
    Grab tweets from queue and write out.
    TODO make turn offable.
    TODO sleep while off?
    """
    fileOut = open('tweetNames.csv', 'w')
    while True:
        if(len(tweetQueue) > 0):
            fileOut.write(tweetQueue.popleft())
            fileOut.write(',')
    fileOut.close()
    
def main(argv):
    """
    Hook up to twitter streaming api and grab all tweets comming from a given
    area.
    """
    #The deque will be sent to the streamer object to collect tweets.
    #the processing end will take tweets and write to output.
    #make two threads, main thread will run streamer, second thread will process tweets.
    tweetQueue = deque()
    #Currently streaming from NYC, no search terms.
    streamer = loginScripts.streamLogin(KEY_FILE_NAME, tweetQueue)
    streamer.statuses.filter(locations=LOC_NYC)

if __name__ == "__main__":
    main(sys.argv[1:])
