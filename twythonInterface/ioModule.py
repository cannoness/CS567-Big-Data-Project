from collections import deque
import json, sys, csv, re

#
#Contains methods for reading and writing to disk.
#

def cleanText(txt):
    """
    This takes a string and takes out anything that is not alpha numeric or ' '.
    @param String txt - String of text to clean.
    @return String Text stripped of characters that are not alphanumeric or ' '.
    """
    keeperChars = '[^0-9a-zA-Z]+'
    txt = txt.strip()
    txt = re.sub(keeperChars, ' ', txt)
    return txt

def jsonToCsv(pathOut, jsonObj):
    """
    Convert a JSON document to csv.
    @param String pathOut - The output path and file name.
    @param json jsonObj - json object containing a list of lists of tweets.
    """
    fOut = open(pathOut, 'w')
    writer = csv.writer(fOut)
    for user in jsonObj:
        for tweet in jsonObj[user]:
            userId = user
            date = tweet['created_at']
            txt = cleanText(tweet['text'])
            writer.writerow((userId, date, txt))
    fOut.close()
    

def writeJson(path, jsonObj):
    """
    Given a path and a json object, write out.
    @param path A string path and filename to write to.
    @param jsonObj A json object to write to file.
    """
    f = open(path, 'w')
    f.write(json.dumps(jsonObj))
    f.close()

def loadJson(path):
    """
    Load a user specified json file.
    @param path A string path and filename for the desired json file.
    @return a json object.
    """
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    return data

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
