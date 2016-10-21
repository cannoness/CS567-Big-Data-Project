from threading import Timer
import loginScripts
import sys, json

class TimelineGrabber():
    """
    Instances of this class grab a users timeline and writes out then sleeps for 15
    minutes.
    TODO make custom timer
    """

    def __init__(self, tickInterval=2.0, grabInterval=15):
        """
        Constructor instatiates class.
        Members:
        int minutesSinceLast:  Number of ticks since last timeline grab.
        int grabInterval: Number of minutes between grabs.
        float tickLength: Number of seconds per tick.
        bool isDone: Flag to set when done grabbing tweets.
        int numGrabs: Number of grabs made so far
        int maxGrabs: Number of sets of grabs to make.
        Twython twyLink: object that will be used to access Twitter timelines

        @param float tickInterval Clock ticks every tickInterval seconds.
        @param int grabInterval Number of clock ticks between timeline grabs.
        """
        self.minutesSinceLast = grabInterval
        self.grabInterval = grabInterval
        self.tickLength = tickInterval
        self.clock = None
        self.isDone = False
        self.numGrabs = 0
        self.maxGrabs = 5 #temporary for testing right now.
        self.twyLink = None
        
    def startTimer(self):
        """
        Method to call to start timer.
        """
        self.clockTick()

    def login():
        """
        TODO
        Login to twitter and get a Twython object
        @param keyFileName Name of the file to login with.
        """
        #get keyFileName
        return loginScripts.searchLogin(keyFileName)

    def getSearchList():
        """
        TODO
        this method returns a list of user names to search for on this grab.
        Should be no larger than 300
        """
        ids = []
        #TODO get ids
        return ids
        
    def getTimelines(ls, twitter):
        """
        TODO
        This method grabs timelines for each user in ls
        Will return data as a list of timelines.
        @param ls list of strings to get user timeline from.
        """
        data = []
        for user in ls:
            #user.toInt
            #get Timeline
            #data.append(twitter.get_user_timeline(user_id=int(user), count=20)) Check when twitter is back up.
            print "Getting timeline ", user #TODO remove
        return data

    def writeData(data):
        """
        TODO
        Dump data into json
        """
        outStr = json.dumps(data)
        #write file.
    
    def clockTick(self):
        """
        This method gets called when there is a clock tick.  Timeline grabber decides if
        it is time to grab again.  If it is not, it prints a heartbeat.
        """        
        if self.minutesSinceLast == self.grabInterval:
            #reset minutes since last, increment number of grabs, call check if done.
            self.minutesSinceLast = 0
            self.numGrabs += 1
            #twitter = login()
            #users = getSearchList()
            #data = getTimelines(users)
            #writeData(data)
            self.checkIfDone()
            print "Grabbing timelines"
        else:
            self.minutesSinceLast += 1
            print self.minutesSinceLast, " minutes since last grab."

        #If not done reset timer and restart.
        if not self.isDone:
            self.clock = Timer(self.tickLength, self.clockTick)
            self.clock.start()

    def checkIfDone(self):
        """
        Method for checking if done testing timer.  Kill the thread by setting
        isDone member variable.
        """
        if self.numGrabs > self.maxGrabs:
            self.isDone = True
