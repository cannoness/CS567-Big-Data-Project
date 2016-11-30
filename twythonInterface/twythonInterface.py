import twythonUtils as tu
import ioModule as output
import json, sys, csv
from collections import deque
from threading import Thread
from pymongo import MongoClient

KEY_FILE_NAME = 'config/keys1.json'
WRITE_PATH = 'output/'
TIMELINE_PATH = WRITE_PATH + 'timelines/'
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
ti.runTimelineGrabber([fileIn], [fileOut], [testing], [startFrom])
  fileIn = String name of file to get user ids from. Default = 'uniqueN.txt'
  fileOut = String base name for files (NO EXTENSION, NO NUMBERS) to write 
    out (json format). Default = 'timeline'
  testing = boolean, if false run with real collection parameters. Default = False
  startFrom = int, start from a grab later than the first.
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

def runTimelineGrabber(inFile='uniqueN.txt', outFile='timeline', testing=False,
                       startFrom=0, isFollowup=False):
    """
    Use this for a live run of the timeline grabber.  Just for convenience.
    @param inFile - Name of input file name.
    @param outFile - Name of output file name base (before extension or number)
    @param testing - False if not a test run.
    @param startFrom - Int what grab to start from (Start later in the id list).
    """
    grabTimelines(inFile, outFile, testing, startFrom, isFollowup)
    
def grabTimelines(ids='uniqueN.txt', fileOut='timeline', testing=True, startFrom=0,
                  isFollowup=False):
    """
    Begin timeline grabbing.
    @param ids - String name of file of ids.
    @param fileOut - String output filename without extension.
    @param testing - Is this a test run? If false set Timeline Grabber's real parameters.
    @param startFrom - Int what grab to start from (Start later in the id list).
    """

    tlg = tu.TimelineGrabber()
    tlg.fileIn = WRITE_PATH + ids
    tlg.fileOut = TIMELINE_PATH + fileOut
    tlg.keyFileName = KEY_FILE_NAME
    tlg.numGrabs = startFrom
    tlg.isFollowup = isFollowup
    
    #if this is a live run set real parameters.
    if not testing:
        tlg.usersPerGrab = 300
        tlg.tweetsPerUser = 100
        tlg.tickLength = 60.0
        tlg.grabInterval = 15
        tlg.minutesSinceLast = 15
        tlg.isTesting = False
    
    tlg.startTimer()

def trimTweets(tlRange=20, isFollowup=False, inFileName='timeline',
               outFileName='timelineT', idFile='followUpIDs'):
    """
    Load json, go through each timeline and trim out tweets outside of range and beyond
    20
    @param int tlRange File number limit (exclusive)
    @param boolean isFollowup Deprecated
    @param String inFileName base timeline in file name
    @param String outFileName base timeline out file name
    @param String idFile Name of file to print follow up ids to
    """
    fNamesIn = output.filenameGenerator(TIMELINE_PATH, inFileName, 0, tlRange, '.json')
    fNamesOut = output.filenameGenerator(TIMELINE_PATH, outFileName, 0, tlRange, '.json')
    followupNames = output.filenameGenerator(WRITE_PATH, idFile, 0, tlRange, '.txt')
    tweetsSaved = 0
    index = -1
    for name in fNamesIn:
        tooNew = False
        
        #fileInName = WRITE_PATH + 'timelines/' + inFileName + str(i) + '.json'
        #fileOutName = WRITE_PATH + 'timelines/' + outFileName + str(i) + '.json'
        #followUpName = WRITE_PATH + idFile + str(i) + '.txt'
        followUps = open(followupNames.next(), 'w') #open file to write follow up ids to.
        timeline = loadJson(name)
        outJson = {}
        for user in timeline:
            tweetsSaved = 0
            newList = []
            for tweet in timeline[user]:
                score = tu.dateInRange(tweet['created_at'])
                lastID = tweet['id_str']
                if score < 0:
                    #last tweet too old
                    print '.',
                elif score > 0:
                    #last tweet too new, flag for followup
                    tooNew = True
                else:
                    if tweetsSaved >= 20:
                        break
                    else:
                        newList.append(tweet)
                        tweetsSaved += 1



            if tweetsSaved < 20 and tooNew:
                followUps.write(user)
                followUps.write(' ')
                followUps.write(str(lastID))
                followUps.write('\n')
            if tweetsSaved > 0:
                outJson[user] = newList
            print "Saved ", len(newList)
        output.writeJson(fNamesOut.next(), outJson)
        followUps.close()
                    
def tweetCreatedSinceAugust(tweet):
    """
    @deprecated
    See if a given tweet was created since 8/2016
    """
    
    months = 'AugSepOctNovDec'
    year = '2016'
    return tu.tweetCreatedSince(tweet, months, year)

def timelinesToCsv(tlRange=20, nameIn='timeline', nameOut='timelines.csv'):
    fOut = open(WRITE_PATH + nameOut, 'w')
    writer = csv.writer(fOut)
    fNamesIn = output.filenameGenerator(TIMELINE_PATH, nameIn, 0, tlRange, '.json')
    for fileName in fNamesIn:
        jsonObj = loadJson(fileName)
        for user in jsonObj:
            for tweet in jsonObj[user]:
                userId = user
                date = tweet['created_at']
                txt = output.cleanText(tweet['text'])
                writer.writerow((userId, date, txt))
    fOut.close()


    
def toCsv(pathIn='output/timelines/tBA0.json', pathOut='output/tBA0.csv'):
    output.jsonToCsv(pathOut, loadJson(pathIn))

def concatenateIDFiles(nameRange=20, inName='followUpIDs', outPath='output/followUpIDs.txt'):
    """
    Concatenate followup id files
    @paramo int nameRange - Maximum range of file numbers (exclusive) default 20
    """
    with open(outPath, 'w') as outFile:
        for i in range(0, nameRange):
            fileName = 'output/' + inName + str(i) + '.txt'
            print fileName
            with open(fileName, 'r') as inFile:
                for line in inFile:
                    outFile.write(line)


def makeBigJson():
    """
    Combine jsons into one json.
    Key is user id_str
    Info saved is text and created at string.
    """
    dataOut = {}
    baseName = 'output/timelines/timelineT'
    extension = '.json'
    for i in range(0, 20):
        fileName = baseName + str(i) + extension
        jsonIn = loadJson(fileName)
        print "Loaded ", fileName, " ", len(jsonIn), " users."
        for user in jsonIn:
            if len(user) > 0:
                idStr = user[0]['user']['id_str']
                tweetList = []
                for tweet in user:
                    entry = {}
                    entry['text'] = tweet['text']
                    entry['created_at'] = tweet['created_at']
                    tweetList.append(entry)
                dataOut[idStr] = tweetList
        print len(dataOut)
    output.writeJson('output/timelines/timelineTBig.json', dataOut)

def addToJson(nameIn='timelineTB', basePath='output/timelines/timelineTBig.json',
              outPath='output/timelines/timelineTBigA0.json', numRange=4):
    """
    Add smaller jsons to large JSON
    #TODO test this.  As of 11/13/2016 1:34pm is untested
    """
    baseJson = loadJson(basePath)
    for i in range(0, numRange):
        fileName = 'output/timelines/' + nameIn + str(i) + '.json'
        jsonIn = loadJson(fileName)
        for user in jsonIn:
            if len(jsonIn[user]) > 0:
                idStr = user
                tweetList = []
                for tweet in jsonIn[user]:
                    entry = {}
                    entry['text'] = tweet['text']
                    entry['created_at'] = tweet['created_at']
                    entry['id'] = tweet['id']
                    tweetList.append(entry)
                if idStr in baseJson:
                    print "ID here ", idStr, " length: ", len(baseJson[idStr])
                    numToTake = 20 - len(baseJson[idStr])
                    baseJson[idStr].extend(tweetList[:numToTake])
                    print "Adding: ", numToTake, "new length: ", len(baseJson[idStr])
                else:
                    baseJson[idStr] = tweetList
    output.writeJson(outPath, baseJson)

def putTweetInDB(tweet):
    """
    This is a test method to insert a tweet, assumes a db on local host
    """
    client = MongoClient()
    db = client['nyTweets']
    collection = db['tweets']
    output.tweetToDB(collection, tweet)
