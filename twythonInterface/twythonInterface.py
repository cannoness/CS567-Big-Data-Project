import twythonUtils as tu
import ioModule as output
import json, sys
from collections import deque
from threading import Thread

KEY_FILE_NAME = 'config/keys1.json'
WRITE_PATH = 'output/'
DEFAULT_FILE_OUT = 'data.json'

LOC_NYC = '-74,40,-73,41'
    
def searchForTerms(term=' ', count=5, writePath=DEFAULT_FILE_OUT):
    """
    Search twitter for a term
    @param term String query.
    @param count int number of results to return.
    @param writePath String path and filename to write to.
    """
    twitter = tu.searchLogin(KEY_FILE_NAME)
    results = twitter.search(q=term, count=count)
    writeJson(WRITE_PATH + writePath, results['statuses'])

def streamIDsTo(fileOut=DEFAULT_FILE_OUT):
    """
    Stream user ids to a file.
    """
    #stream python ids
    tweetQ = deque()
    writer = output.IDWriter(tweetQ)
    tweetStream = Thread(target=tu.startLocStream, args=(tweetQ, LOC_NYC, KEY_FILE_NAME))
    tweetStream.daemon = True
    tweetStream.start()

    writer.writeIDs(WRITE_PATH + fileOut)
