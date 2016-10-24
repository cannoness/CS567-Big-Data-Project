import twythonUtils as tu
import ioModule as output
import json, sys
from collections import deque
from threading import Thread

KEY_FILE_NAME = 'config/keys1.json'
WRITE_PATH = 'output/'
DEFAULT_FILE_OUT = 'data.json'

LOC_NYC = '-74,40,-73,41'
    
def searchForTerms(term=' ', count=5, fileName=DEFAULT_FILE_OUT):
    """
    Search twitter for a term.  Output json to output/fileName.
    @param term String query.
    @param count int number of results to return.
    @param writePath String path and filename to write to.
    """
    twitter = tu.searchLogin(KEY_FILE_NAME)
    results = twitter.search(q=term, count=count)
    writeJson(WRITE_PATH + writePath, results['statuses'])

def streamIDsTo(fileOut=DEFAULT_FILE_OUT, loc=LOC_NYC):
    """
    Stream user ids to output/fileOut
    """
    #stream python ids
    tweetQ = deque()
    writer = output.IDWriter(tweetQ)
    tweetStream = Thread(target=tu.startLocStream, args=(tweetQ, loc, KEY_FILE_NAME))
    tweetStream.daemon = True
    tweetStream.start()

    writer.writeIDs(WRITE_PATH + fileOut)

def grabTimelines(ids='uniqueN.txt', fileOut='timeline'):

    tlg = tu.TimelineGrabber()
    tlg.fileIn = WRITE_PATH + ids
    tlg.fileOut = WRITE_PATH + fileOut
    tlg.keyFileName = KEY_FILE_NAME
    
    tlg.startTimer()
    
