#this is a class
#contains a timer.

from threading import Timer

class TimelineGrabber():
    """
    Instances of this class grab a users timeline and writes out then sleeps for 15
    minutes.
    """

    def __init__(self):
        """
        Constructor creates an instance of the class.  Instantiates timer.
        """
        self.minutesSinceLast = 15
        
