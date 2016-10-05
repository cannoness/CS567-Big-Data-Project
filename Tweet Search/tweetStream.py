from MyStreamer import MyStreamer
from twython import Twython
import loginScripts
import sys
import json

#
# Driver to hook up to python stream.
# currently collecting tweets around NYC
# TODO Take args and collect tweets around various areas
#

KEY_FILE_NAME = 'keys1.json'
#string creating bounding box around NYC
LOC_NYC = '-74,40,-73,41'
def main(argv):
    """
    Hook up to twitter streaming api and grab all tweets comming from a given
    area.
    """
    #Currently streaming from NYC, no search terms.
    streamer = loginScripts.streamLogin(KEY_FILE_NAME)
    streamer.statuses.filter(locations=LOC_NYC)

if __name__ == "__main__":
    main(sys.argv[1:])
