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
def startStream(tweetQ):
    streamer = loginScripts.streamLogin(KEY_FILE_NAME, tweetQ)
    streamer.statuses.filter(locations=LOC_NYC)
    

def main(argv):
    """
    Hook up to twitter streaming api and grab all tweets comming from a given
    area.
    """
    #The deque will be sent to the streamer object to collect tweets.
    #the processing end will take tweets and write to output.
    #make two threads, main thread will run streamer, second thread will process tweets.
    tweetQueue = deque()
    #TODO, make thread to write on
    writer = IDWriter(tweetQueue)
    tweetStream = Thread(target=startStream, args=(tweetQueue,))
    tweetStream.daemon = True
    tweetStream.start()
    writer.writeIDs(OUTPUT_FILE_NAME)
    #Currently streaming from NYC, no search terms.
    

if __name__ == "__main__":
    main(sys.argv[1:])
