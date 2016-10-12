from MyStreamer import MyStreamer
from IDWriter import IDWriter
from twython import Twython
from collections import deque
from threading import Thread
import loginScripts
import sys
import json

#
# Driver to hook up to python stream.
# currently collecting tweets around NYC
# TODO Take args and collect tweets around various areas
#

KEY_FILE_NAME = 'keys1.json'
OUTPUT_FILE_NAME = 'ids.csv'
#string creating bounding box around NYC
LOC_NYC = '-74,40,-73,41'
def startStream(tweetQ, loc=LOC_NYC):
    """
    This method creates a MyStreamer object and starts streaming from twitter.
    This method should be called as the target of a thread.
    @param tweetQ deque that is passed on to the MyStreamer constructor to be used to
                  collect streams as they come in.
    @param loc String string constructing bounding box of areas to stream from. Default
                  to NEW YAWK CITEH!?!?!?
    """
    streamer = loginScripts.streamLogin(KEY_FILE_NAME, tweetQ)
    streamer.statuses.filter(locations=loc)
    

def main(argv):
    """
    Hook up to twitter streaming api and grab all tweets comming from a given
    area.
    """
    #The deque will be sent to the streamer object to collect tweets.
    tweetQueue = deque()

    #ID writer will handle writing tweets to output file.
    writer = IDWriter(tweetQueue)

    #the twitter stream goes on its own thread.
    tweetStream = Thread(target=startStream, args=(tweetQueue,))
    #set daemon flag to true, this will cause thread to stop when python exits.
    tweetStream.daemon = True
    tweetStream.start()

    #with stream started, begin writing output files.
    writer.writeIDs(OUTPUT_FILE_NAME)

    

if __name__ == "__main__":
    main(sys.argv[1:])
