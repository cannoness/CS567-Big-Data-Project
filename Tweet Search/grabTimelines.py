import sys
from TimelineGrabber import TimelineGrabber

def testGrab(tickInterval, grabInterval):
    """
    Test the timer with user defined intervals.
    """
    grabber = TimelineGrabber(tickInterval, grabInterval)
    grabber.startTimer()
    
def beginGrabbing():
    """
    Begin grabbing timelines from twitter.
    Currently testing.
    """
    #grab 300 timelines,
    #write out
    #sleep 15 min
    grabber = TimelineGrabber()
    grabber.startTimer()
