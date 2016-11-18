from twython import Twython, TwythonError, TwythonRateLimitError
from twython import TwythonStreamer
from collections import deque
from threading import Thread
from threading import Timer
import ioModule as output
import json, sys, time



def startLocStream(tweetQ, loc, keyfile):
    """
    This method creates a MyStreamer object and starts streaming from twitter.
    This method should be called as the target of a thread.
    @param tweetQ deque that is passed on to the MyStreamer constructor to be used to
                  collect streams as they come in.
    @param loc String string constructing bounding box of areas to stream from. Default
                  to NEW YAWK CITEH!?!?!?
    """
    streamer = streamLogin(keyfile, tweetQ)
    streamer.statuses.filter(locations=loc)

def dateInRange(dateString):
    """
    Return true if date string is in range. Using Nov strictly less than Nov 7 to cut
    last minute get out the vote stuff.
    @return int isValid - if isValid is negative, tweet is too old, if positive too new
    0 is in valid range.
    """
    dateArr = dateString.split()
    isValid = -1
    if dateArr[5] == '2016':
        if dateArr[1] in 'AugSepOct':
            isValid = 0
        elif dateArr[1] == 'Nov' and int(dateArr[2]) < 7:

            isValid = 0
        else:
            #Tweet came too late.  Flag to search farther back.
            #save tweet id
            isValid = 1
    return isValid

        
def tweetCreatedSince(tweet, months, year):
    """
    @deprecated
    Check if tweet was created since a user specified month.
    @param Tweet tweet - Tweet object (json format).
    @param String months - Month names that are valid.
    @param String year - Year that we're looking in.
    @return - True if tweet was created within time limit.
    """
    #monthString = 'AugSepOctNovDec'
    #yearString = '2016'
    tweetDate = tweet['created_at']
    dateArr = tweetDate.split()
    isValid = False
    if dateArr[1] in months and dateArr[5] == year:
        isValid = True

    return isValid
    #return is valid since

#********* Login functions**********************************************************
# Use streamLogin to use TwythonStreamer.
# Use searchLogin to perform a search.
#
# Justin Thomas
# 10/05/2016
#

#These variables store the names of the keyFile entry tags.
CONSUMER_KEY = 'consumerKey'
CONSUMER_SECRET = 'consumerSecret'
ACCESS_TOKEN = 'accessToken'

def streamLogin(KEY_FILE_NAME, tweetQ):
    """
    Login to twitter, authorize and return MyStreamer, twitter streaming object.
    @param KEY_FILE_NAME String: Name of file containing the consumer key and secret.
    @param tweetQ: Deque for holding incomming tweets awaiting processing.  This is
                   to be passed along to the streaming object.
    @return MyStreamer object, extends TwythonStreamer
    """

    keyFile = json.load(open(KEY_FILE_NAME))
    #read consumer key, strip trailing whitespace.
    APP_KEY = keyFile[CONSUMER_KEY]
    #read consumer secret, strip trailing whitespace.
    APP_SECRET = keyFile[CONSUMER_SECRET]
    #create Twython instance to get oauth tokens.
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_SECRET = auth['oauth_token_secret']

    #prompt user to go to url and get PIN entry.
    print "\n\n\nGo to the following url and enter the PIN you find there."
    print auth['auth_url']
    verifier = raw_input()

    #get final OAUTH token and secret.
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
    finalStep = twitter.get_authorized_tokens(verifier)
    OAUTH_TOKEN = finalStep['oauth_token']
    OAUTH_SECRET = finalStep['oauth_token_secret']

    return MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET, tweetQ)

def searchLogin(KEY_FILE_NAME):
    """
    Return a Twython object to perform a search.
    @param KEY_FILE_NAME String: name of the file with the keys.
    @return Twython object.
    """
    keyFile = json.load(open(KEY_FILE_NAME))
    return Twython(keyFile[CONSUMER_KEY], access_token=keyFile[ACCESS_TOKEN])

#***********************Begin Classes**************************************************


#****My Streamer******************
class MyStreamer(TwythonStreamer):
    """
    MyStreamer class extends twython streamer.  This class will log user ids in a
    newline delimited file and save them for later analysis.

    Justin Thomas
    10/05/2016
    """

    def __init__(self, appKey, appSecret, oauthToken, oauthSecret, tweetQ=None):
        """
        Constructor.  Calls superclass, and saves reference to the tweet queue.
        @param deque The deque that will recieve user id_str data and write to a file.
        """
        super(MyStreamer, self).__init__(appKey, appSecret, oauthToken, oauthSecret)
        self.tweetQueue = tweetQ

    def on_success(self, data):
        """
        Implementation of TwythonStreamer API method.
        When the streamer gets a success code, grab id_str and push on tweet deque.
        an instance of IDWriter has a copy of this and will be popping from the other
        end.
        """
        if 'text' in data:
            self.tweetQueue.append(data['user']['id_str'])
            #print json.dumps(data['user']['name'])
            #print json.dumps(data['text'])

    def on_error(self, status_code, data):
        """
        TODO handle twitter API errors.
        """
        print status_code, data
        #self.disconnect()

#******TimelineGrabber*******************
class TimelineGrabber():
    """
    Instances of this class grab a users timeline and writes out to json then sleeps 
    for 15 minutes before writing again.
        Members:
        int minutesSinceLast:  Number of ticks since last timeline grab.
        int grabInterval: Number of minutes between grabs.
        float tickLength: Number of seconds per tick.
        bool isDone: Flag to set when done grabbing tweets.
        int numGrabs: Number of grabs made so far
        int maxGrabs: Number of sets of grabs to make (testing).
        int usersPerGrab: Number of timelines to grab at a time.
        int tweetsPerUser: Number of tweets in timeline to grab.
        String fileIn: File name and path to get user ids from.
        String fileOut: Path and file name base to write to (no extension, no number).
        String keyFileName: Path and name of login keys.


    """

    def __init__(self, tickInterval=1.0, grabInterval=5):
        """
        Constructor instatiates class.
        @param float tickInterval - Clock ticks every tickInterval seconds.
        @param int grabInterval - Number of clock ticks between timeline grabs.
        """
        self.minutesSinceLast = grabInterval
        self.grabInterval = grabInterval
        self.tickLength = tickInterval
        self.clock = None
        self.isDone = False
        self.numGrabs = 0
        self.maxGrabs = 1 #temporary for testing right now.
        self.usersPerGrab = 3
        self.tweetsPerUser = 3
        self.fileIn = None
        self.fileOut = None
        self.keyFileName = None
        self.isTesting = True
        self.isFollowup = False

    def startTimer(self):
        """
        Method to call to start timer. and thus start grabbing.
        """
        self.clockTick()

    def login(self):
        """
        Login to twitter and get a Twython object
        @param keyFileName Name of the file to login with.
        @return Twitter object to use.
        """
        #get keyFileName
        return searchLogin(self.keyFileName)

    def getSearchList(self):
        """
        This method returns a list of user names to search for on this grab.
        Should be no larger than 300.
        @return list of user ids to get timelines from
        """
        ids = []
        f = open(self.fileIn, 'r')
        startAt = self.numGrabs * self.usersPerGrab
        
        #skip ids that have already been read.
        for _ in xrange(startAt):
            f.readline()
        #make list of user ids to get timelines from.    
        for _ in xrange(self.usersPerGrab):
            usrID = f.readline().split()
            if len(usrID) != 0:
                ids.append(usrID)
            else:
                print "End of id file"
                break
        return ids
        
    def getTimelines(self, ls, twitter):
        """
        This method grabs timelines for each user in ls
        Will return data as a list of timelines.
        @param ls list of strings to get user timeline from.
        """
        data = {}
        print "Getting timelines for ", len(ls), " users."
        for user in ls:
            try:
                idStr=user[0]
                #If this is a followup, call api with max_id set
                if self.isFollowup:
                    if len(user) >= 2:
                        timeline = twitter.get_user_timeline(user_id=idStr,
                                                             count = self.tweetsPerUser,
                                                             trim_user=True,
                                                             max_id=user[1])
                    else:
                        print "User did not have max_id"
                else:
                    timeline = twitter.get_user_timeline(user_id=idStr,
                                                     count=self.tweetsPerUser,
                                                     trim_user=True)
                tweets = []
                for tweet in timeline:
                    entry = {}
                    entry['user_id'] = tweet['user']['id_str']#user id
                    entry['created_at'] = tweet['created_at']
                    entry['text'] = tweet['text']
                    entry['id_str'] = tweet['id_str']#tweet id
                    tweets.append(entry)
                data[idStr] = tweets
            except TwythonRateLimitError as e:
                #This occurs when a rate limit error is thrown.
                #at this point, the program steps out of the loop and resumes pickup on
                #the next scheduled grab.
                print e
                print "Rate limit, stepping out of loop..."
                break
            except TwythonError as e:
                #on error, print user that threw error and continue.
                #TODO log errors?
                print e
                print "User id: ", user
    
        print "Got timelines for ", len(data), " users."
        return data

    def writeData(self, data):
        """
        write data to json
        """
        path = self.fileOut + str(self.numGrabs) + '.json'
        output.writeJson(path, data)

    def clockTick(self):
        """
        This method gets called when there is a clock tick.  Timeline grabber decides if
        it is time to grab again.  If it is not, it prints a heartbeat.
        """        
        if self.minutesSinceLast == self.grabInterval:

            self.minutesSinceLast = 0
            twitter = self.login()
            users = self.getSearchList()

            #If less than 300 users are in the list, this must be the last grab.
            if len(users) < self.usersPerGrab:
                print "User list is smaller than ", self.usersPerGrab, "Set flag, isDone"
                self.isDone = True
            data = self.getTimelines(users, twitter)
            self.writeData(data)

            #done check for premature termination in testing.
            if self.isTesting:
                self.checkIfDone()
            
            self.numGrabs += 1
            print "Made ", str(self.numGrabs), " so far."
            
        else: #heartbeat
            self.minutesSinceLast += 1
            print self.minutesSinceLast, " minutes since last grab."

        #If not done reset timer and restart.
        if not self.isDone:
            print "Starting clock"
            self.clock = Timer(self.tickLength, self.clockTick)
            self.clock.daemon=True #Stop timer on exit()
            self.clock.start()

    def checkIfDone(self):
        """
        Method for checking if done testing timer.  Kill the thread by setting
        isDone member variable.
        """
        if self.numGrabs > self.maxGrabs:
            self.isDone = True
