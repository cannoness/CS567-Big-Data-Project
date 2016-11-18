# Written by Vanessa Job, November 18, 2016.  Based on code by Rudy Martinez.   The mongodb database is his!
from pymongo import MongoClient
from pprint import pprint
import time

if __name__ == '__main__':
    #Set up connection to Mongo client. 
    client = MongoClient("mongodb://rudym:cs567rm@mongodb.cs.unm.edu:27017")
    db = client['USATweets']

    #Retrieve count.  We don't need it, but it's interesting.  
    numRecords = db.tweets.count()
    #print(numRecords)

    #Find all records that tweet['user']['id_str'] and tweet['id_str'].  The incomplete ones get ignored. 
    tweetRecords = db.tweets.find()   # This grabs all the tweets. 
    for document in tweetRecords:
	try:
       	     print str(document['user']['id_str']),str(document['id_str'])
	except Exception:
		pass

