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

def runTimelineGrabber(inFile='uniqueN.txt', outFile='timeline', testing=False):
    """
    Use this for a live run of the timeline grabber.  Just for convenience.
    @param inFile - Name of input file name.
    @param outFile - Name of output file name base (before extension or number)
    @param testing - False if not a test run.
    """
    grabTimelines(inFile, outFile, testing)
    
def grabTimelines(ids='uniqueN.txt', fileOut='timeline', testing=True):
    """
    Begin timeline grabbing.
    @param ids - String name of file of ids.
    @param fileOut - String output filename without extension.
    @param testing - Is this a test run? If false set Timeline Grabber's real parameters.
    """

    tlg = tu.TimelineGrabber()
    tlg.fileIn = WRITE_PATH + ids
    tlg.fileOut = WRITE_PATH + 'timelines/' + fileOut
    tlg.keyFileName = KEY_FILE_NAME
    
    #if this is a live run set real parameters.
    if not testing:
        tlg.usersPerGrab = 300
        tlg.tweetsPerUser = 20
        tlg.tickLength = 60.0
        tlg.grabInterval = 15
        tlg.minutesSinceLast = 15
        tlg.isTesting = False
    
    tlg.startTimer()
    
