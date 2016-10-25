import twythonUtils as tu
import ioModule as output
import json, sys
from collections import deque
from threading import Thread

KEY_FILE_NAME = 'config/keys1.json'
WRITE_PATH = 'output/'
DEFAULT_FILE_OUT = 'data.json'

LOC_NYC = '-74,40,-73,41'

help_searchTerm = '''
To search for term use:
ti.searchForTerms([term], [count], [fileName])
  term = String search term. Default = ' '
  count = int number of tweets to return. Default = 5
  fileName = Name of file (and extension) to output to (json format) 
    Default = 'data.json'.
'''

help_streamIDs = '''
To stream user ids to a file use:
ti.streamIDsTo([fileOut], [location])
  fileOut = String name of file(and extension) to write to (json format)
    Default = 'data.json'.
  location = String describing bounding box of area to stream tweets from.
    Default = Bounding box around New York City provided by twitter documentation.
'''

help_timelines = '''
To grab user timelines use:
ti.runTimelineGrabber([fileIn], [fileOut], [testing])
  fileIn = String name of file to get user ids from. Default = 'uniqueN.txt'
  fileOut = String base name for files (NO EXTENSION, NO NUMBERS) to write 
    out (json format). Default = 'timeline'
  testing = boolean, if false run with real collection parameters. Default = False
'''

help_loadJson = '''
To load a json file to look at manually use:
ti.loadJson([filePath])
  filePath = String file path/name to load. Default = None (Will cause error).
'''

def man():
    """
    How to use instructions.
    """
    print help_searchTerm
    print help_streamIDs
    print help_timelines
    print help_loadJson

def loadJson(filePath):
    """
    Load a json file to interpreter for manual reading.
    @return json object
    """
    return output.loadJson(filePath)
    
    
def searchForTerms(term=' ', count=5, fileName=DEFAULT_FILE_OUT):
    """
    Search twitter for a term.  Output json to output/fileName.
    @param term String query.
    @param count int number of results to return.
    @param writePath String path and filename to write to.
    """
    twitter = tu.searchLogin(KEY_FILE_NAME)
    results = twitter.search(q=term, count=count)
    output.writeJson(WRITE_PATH + fileName, results['statuses'])

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
