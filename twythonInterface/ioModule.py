from collections import deque
import json, sys

#
#Contains methods for reading and writing to disk.
#

def writeJson(path, jsonObj):
    """
    Given a path and a json object, write out.
    @param path A string path and filename to write to.
    @param jsonObj A json object to write to file.
    """
    f = open(path, 'w')
    f.write(json.dumps(jsonObj))
    f.close()

class IDWriter:
    """
    This class watches a deque of twitter user ids and writes the IDs out as a 
    newline delimited file.
    To be processed on hdfs to create a list of unique users.
    """

    def __init__(self, tweetQ):
        """
        Constructor for IDWriter.  Saves a reference to the deque that user id strings
        are put in to
        @param tweetQ deque that user IDs will come in through.
        """
        self.tweetQueue = tweetQ

    def writeIDs(self, fileName):
        """
        Grab an ID from tweetQueue and write out, should be run on a separate thread.
        TODO make turn offable.
        TODO sleep while off?
        TODO backup periodically?
        """
        fileOut = open(fileName, 'w')
        while True:
            if(len(self.tweetQueue) > 0):
                fileOut.write(self.tweetQueue.popleft())
                fileOut.write('\n')
        fileOut.close()
