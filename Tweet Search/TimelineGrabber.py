#this is a class
#contains a timer.

from threading import Timer

class TimelineGrabber():
    """
    Instances of this class grab a users timeline and writes out then sleeps for 15
    minutes.
    TODO make custom timer
    """

    def __init__(self):
        """
        Constructor instatiates class.
        Members:
        minutesSinceLast.  Number of minutes since last tick.
        """
        self.minutesSinceLast = 15
        self.clock = None
        self.isDone = False
        self.numGrabs = 0
        self.maxGrabs = 5 #temporary for testing right now.
        
    def startTimer(self):
        """
        Start the timer.
        """
        self.clockTick()
        
    def clockTick(self):
        """
        This method gets called when there is a clock tick.  Timeline grabber decides if
        it is time to grab again or prints heartbeat.
        """
 
        
        if self.minutesSinceLast == 15:
            #grab timelines
            self.minutesSinceLast = 0
            self.numGrabs += 1
            self.checkIfDone()
            print "Grabbing timelines"
        else:
            self.minutesSinceLast += 1
            print self.minutesSinceLast, " minutes since last grab."

        #reset timer and restart.
        if not self.isDone:
            self.clock = Timer(2.0, self.clockTick)
            self.clock.start()

    def checkIfDone(self):
        """
        Method for checking if done testing timer.  Kill the thread by setting
        isDone member variable.
        """
        if self.numGrabs > self.maxGrabs:
            self.isDone = True
