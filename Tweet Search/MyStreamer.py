from twython import TwythonStreamer
from collections import deque
import json

class MyStreamer(TwythonStreamer):
    """
    MyStreamer class extends twython streamer.
    Currently printing out name and text.
    TODO output to file?

    Justin Thomas
    10/05/2016
    """

    def __init__(self, appKey, appSecret, oauthToken, oauthSecret, tweetQ=None):
        super(MyStreamer, self).__init__(appKey, appSecret, oauthToken, oauthSecret)
        self.tweetQueue = tweetQ

    def on_success(self, data):
        """
        When the streamer gets a success code, do this.
        """
        if 'text' in data:
            self.tweetQueue.append(data)
            #TODO remove prints.
            print json.dumps(data['user']['name'])
            print json.dumps(data['text'])

    def on_error(self, status_code, data):
        print status_code, data
        #self.disconnect()
