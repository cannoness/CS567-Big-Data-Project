import json, sys

USAGE_STRING = 'usage: jsonReader.py <file name>'
def main(argv):
    """
    This script reads in a user specified json file an attempts to spit out
    the user name field and the Tweet text.
    """
    if len(sys.argv) == 2:
        fileName = argv[0]
    else:
        print USAGE_STRING
        sys.exit(2)

    fileIn = open(fileName, 'r')
    jdata = json.load(fileIn)
    for entry in jdata:
        print entry['user']['name']
        print entry['text']

if __name__ == "__main__":
    main(sys.argv[1:])
