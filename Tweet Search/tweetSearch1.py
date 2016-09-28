import json, sys, getopt
from twython import Twython


KEY_FILE_NAME = 'start_codes.txt'
USAGE_STRING = """usage: tweetSearch1.py -s <search term> -f <output file> \
[-n <number of tweets to get>]"""

#this script will search twitter for user defined keywords.

def main(argv):
    """
    Take a search term and output file name and search twitter for the term
    User can optionally provide a number of tweets to grab as well.  The default
    number is 5.

    To run:
    python tweetSearch1.py -s <search term> -f <output file> [-n <number of results>]

    Required libraries: json, sys, getopt (default libs?)
    Twython

    Built for Python 2.7.12
    Justin Thomas jthomas105@unm.edu
    """
    searchTerm = ''
    fileOut = ''
    numHits = 5
    try:
        opts, args = getopt.getopt(argv, "hs:f:n:", 
                                   ["searchTerm=", "fileOut=", "numTweets="])
    #in case of argument errors.
    except getopt.GetoptError:
        argError()
    for opt, arg in opts:
        #collect provided arguments.
        if opt in ("-s", "--searchTerm"):
            searchTerm = arg
        elif opt in ("-f", "--fileOut"):
            fileOut = arg
        #help option.
        elif opt == '-h':
            print USAGE_STRING
            sys.exit()
        #if number of tweets to get is provided.
        elif opt in ("-n", "--numTweets"):
            try:
                numHits = int(arg)
                if numHits < 1:
                    argError()
            except ValueError:
                argError()


    """
    If searchTerm and fileOut have been entered properly.  Log in to twitter and 
    search for results.
    """
    if searchTerm and fileOut:
        twitter = login()
        results = twitter.search(q=searchTerm, count=numHits)
        f = open(fileOut, 'w')
        #write the tweet portion of the search out to a file.
        f.write(json.dumps(results['statuses']))
    else:
        argError()


def argError():
    """
    If there was a problem with arguments, we go here.
    """
    print 'There was a problem with provided arguments.'
    print USAGE_STRING
    sys.exit(2)

def login():
    """
    Login method reads in the App key and access token from the appropriate textfile.
    The text file must be formatted so that the app key is on the first line and
    the access token is on the second line.

    KEY_FILE_NAME is currently hard coded.
    
    return: twitter object for performing search.
    """
    APP_KEY = ''
    ACCESS_TOKEN = ''
    
    keyFile = open(KEY_FILE_NAME)
    APP_KEY = keyFile.readline()
    ACCESS_TOKEN = keyFile.readline()
    keyFile.close()
    
    return Twython(APP_KEY, access_token=ACCESS_TOKEN)


    

if __name__ == "__main__":
    main(sys.argv[1:])
