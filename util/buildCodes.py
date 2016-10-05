from twython import Twython
import json
import sys

K_C_KEY = 'consumerKey'
K_C_SECRET = 'consumerSecret'
K_ACCESS_TOKEN = 'accessToken'

#
#How to Use:
#
# You should create a plain text file with your consumer key on the first line and
# consumer secret on the second line.
# 
#run python
#At python prompt type:
#
# import buildCodes
# buildCodes.buildCodeFile('yourConsumerKeyFileName', 'yourDesiredOutputFileName')
# exit()
#
# As of this writing, all files that use the keys are expecting to use a key file
# named 'keys1.json', so this should be 'yourDesiredOutputFileName'.
#
# Justin Thomas
# 10/05/2016
#
def startKeyFile(CONS_KEY_FILENAME):
    """
    Create a keyFile .json.
    @param CONS_KEY_FILENAME Name of a file containing consumer key and consumer secret.
        The first line is Consumer key, and the second is the consumer secret.
    @return keyDict Dictionary containing the keys.
    """
    keyDict = {}
    consKeyFile = open(CONS_KEY_FILENAME, 'r')
    consKey = consKeyFile.readline().rstrip()
    consSecret = consKeyFile.readline().rstrip()
    keyDict[K_C_KEY] = consKey
    keyDict[K_C_SECRET] = consSecret
    keyDict[K_ACCESS_TOKEN] = None
    return keyDict

def getAccessToken(keyDict):
    """
    Take a dictionary and obtain the twitter access token for oauth2
    @param KEYFILE_JSON Name of the file that has the json with the keyfiles.
    """
    twitter = Twython(keyDict[K_C_KEY], keyDict[K_C_SECRET], oauth_version=2)
    keyDict[K_ACCESS_TOKEN] = twitter.obtain_access_token()

def writeKeyDict(keyDict, fileName):
    """
    Write the key dictionary as a json file.
    """
    fileOut = open(fileName, 'w')
    fileOut.write(json.dumps(keyDict))
    fileOut.close()

def buildCodeFile(consumerKeyName, outputFileName):
    """
    Catch all build file function.
    @param consumerKeyName String that is the name of the file containing the
        consumer key and the consumer secret.
    @param outputFileName String that is the desired name of the output file.
    """
    keyDict = startKeyFile(consumerKeyName)
    getAccessToken(keyDict)
    writeKeyDict(keyDict, outputFileName)
