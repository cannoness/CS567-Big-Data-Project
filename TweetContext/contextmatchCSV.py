import csv

#have to initialize since PT won't be initialized if no tweet matches!
tweet_count = PT = NPT = 0
user_tweets = []
print_out = []

#loading up the file to get comparison words from
context_file = open("contextwords.dat", "r")
context_array = context_file.read()
context_list = [s.strip().lower() for s in context_array.splitlines()]
context_file.close()
last_user = ' '

#simple 'stupid' code for comparing strings...
with open('tweetfile.csv', 'rb') as csvfile:
    input_file = csv.reader(csvfile)
    first = True
    for row in input_file:
        current_user = row[0]
        tweet_count += 1
        if current_user == last_user or first:
            for word in row[2].split(" "):
                if word.lower() in context_list:
                    print_out.append([current_user,row[2]])
                    PT += 1
                    break
            last_user = current_user
            first = False
        else:
            user_tweets.append([last_user, PT, tweet_count])
            PT = tweet_count = 0
            for word in row[2].split(" "):
                if word.lower() in context_list:
                    print_out.append([current_user,row[2]])
                    PT += 1
                    break
            last_user = current_user
            
#k now save that shiz
outfile = 'political_data.csv'
with open(outfile, 'wb') as csvfile:
    writer = csv.writer(csvfile,  quoting=csv.QUOTE_ALL)
    for item in user_tweets:
        #Write item to outcsv
        writer.writerow([item[0], item[1],item[2]])
		
outfile = 'political_tweet.csv'
with open(outfile, 'wb') as csvfile:
    writer = csv.writer(csvfile,  quoting=csv.QUOTE_ALL)
    for item in print_out:
        #Write item to outcsv
        writer.writerow([item[0],item[1]])
