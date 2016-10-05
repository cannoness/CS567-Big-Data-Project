from twython import TwythonStreamer
import json

class MyStreamer(TwythonStreamer):
    """
    MyStreamer class extends twython streamer.
    Currently printing out name and text.
    TODO output to file?

    Justin Thomas
    10/05/2016
    """

    def __init__(self, appKey, appSecret, oauthToken, oauthSecret):
        super(MyStreamer, self).__init__(appKey, appSecret, oauthToken, oauthSecret)

    def on_success(self, data):
        if 'text' in data:
            print json.dumps(data['user']['name'])
            print json.dumps(data['text'])
            #fileOut = open('testOut.json', 'w')
            #fileOut.write(json.dumps(data))
            #fileOut.close()
            #self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data
        #self.disconnect()
