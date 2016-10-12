from twython import TwythonStreamer

import json

class JustIdStreamer(TwythonStreamer):
    """
    JustIdStreamer class extends twython streamer.
    Currently printing out just the id from each tweet.  
    TODO output to file?

    JustIdStreamer is a modified version of MyStreamer.py which was created by Justin Thomas on 10/5/2016. 
    Created by Vanessa Job on 10/8/2016

    """



    def __init__(self, appKey, appSecret, oauthToken, oauthSecret):
        super(JustIdStreamer, self).__init__(appKey, appSecret, oauthToken, oauthSecret)
        #super(MyStreamer, self).__init__(appKey, appSecret, oauthToken, oauthSecret)


    def on_success(self, data):
        if 'text' in data:
            #  Here we use the id_str instead of the id.  The id can be an extremely
            # long number.  Some packages can't handle numbers this big. 
            # If you want to use the id instead, uncomment the following line. 
	    #print json.dumps(data['user']['id'])
            with open('file.txt', 'a') as f: 
                some_id = json.dumps(data['user']['id_str'])
            	# print json.dumps(data['user']['id_str'])
                print some_id

		f.write (some_id + "\n")
		#f.close()

		
            #print json.dumps(data['user']['name'])
            #print json.dumps(data['text'])
            #fileOut = open('testOut.json', 'w')
            #fileOut.write(json.dumps(data))
            #fileOut.close()
            #self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data
        #self.disconnect()
