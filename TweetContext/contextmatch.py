import json

#have to initialize since PT won't be initialized if no tweet matches!
PT = NPT = 0

#loading up the file to get comparison words from
context_file = open("contextwords.dat", "r")
context_array = context_file.read()
context_list = [s.strip().lower() for s in context_array.splitlines()]
context_file.close()

#simple 'stupid' code for comparing strings...
jdata = json.load(open("testtweet.json", 'r'))

#this is a test of the "stupid" code showing it does not seek misspellings,uncomment this and the first forloop to test
#jdata =  ["this is a test tweet with Hillary name in it", "this is a test with a mispelled hilary"] 

for tweet in jdata:
    #for word in tweet.split(" "):
    for word in tweet['text'].split(" "):
        if word.lower() in context_list:
            PT += 1
            break
            
#seriously, the easiest way to count non-political tweets since we terminate the loop early when a political thing is found.            
NPT = len(jdata)-PT
print PT, NPT