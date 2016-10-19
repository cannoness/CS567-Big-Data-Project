from twython import TwythonStreamer
from collections import deque
import json

class MyStreamer(TwythonStreamer):
    """
    MyStreamer class extends twython streamer.
    Currently printing out name and text.

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
