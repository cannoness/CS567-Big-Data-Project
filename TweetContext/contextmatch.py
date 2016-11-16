import json
import csv

#have to initialize since PT won't be initialized if no tweet matches!
tweet_count = PT = NPT = 0
user_tweets = []

#loading up the file to get comparison words from
context_file = open("TweetContext\contextwords.dat", "r")
context_array = context_file.read()
context_list = [s.strip().lower() for s in context_array.splitlines()]
context_file.close()
print_out = []
#simple 'stupid' code for comparing strings...
jdata = json.load(open("timelineBig.json", 'r'))

#this is a test of the "stupid" code showing it does not seek misspellings,uncomment this and the first forloop to test
#jdata =  ["this is a test tweet with Hillary name in it", "this is a test with a mispelled hilary"] 
for user in jdata:
    for tweet in user:
        tweet_count += 1
        #for word in tweet.split(" "):
        for word in tweet['text'].split(" "):
            if word.lower() in context_list:
                print_out.append(tweet['text'])
                PT += 1
                break
    user_tweets.append([PT, tweet_count])
    PT = tweet_count = 0
                
#seriously, the easiest way to count non-political tweets since we terminate the loop early when a political thing is found.            
NPT = len(jdata)-PT
print PT, NPT

#k now save that shiz
outfile = 'political_data.csv'
with open(outfile, 'wb') as csvfile:
    writer = csv.writer(csvfile,  quoting=csv.QUOTE_ALL)
    for item in user_tweets:
        #Write item to outcsv
        writer.writerow([item[0], item[1]])

outfile = 'political_tweet.csv'
with open(outfile, 'wb') as csvfile:
    writer = csv.writer(csvfile,  quoting=csv.QUOTE_ALL)
    for item in print_out:
        #Write item to outcsv
        writer.writerow(item)