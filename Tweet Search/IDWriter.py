from collections import deque

class IDWriter:
    """
    This class watches a deque of twitter user ids and writes the IDs out as a CSV
    To be processed on hdfs to create a list of unique users.
    """

    def __init__(self, tweetQ):
        """
        Constructor for IDWriter.
        @param tweetQ deque that user IDs will come in through.
        """
        self.tweetQueue = tweetQ

    def writeIDs(self, fileName):
        """
        Grab an ID from tweetQueue and write out, should be run on a separate thread.
        TODO make turn offable.
        TODO sleep while off?
        """
        fileOut = open(fileName, 'w')
        while True:
            if(len(self.tweetQueue) > 0):
                fileOut.write(self.tweetQueue.popleft())
                fileOut.write(',')
        fileOut.close()
