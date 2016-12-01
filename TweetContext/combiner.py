import csv

sent_array = []
pol_array = []
user_sent_first_only = []
user_sent_averaged = []
clinton = trump = 0

with open('out.csv', 'rb') as sentfile:
    input_file = csv.reader(sentfile)
    for row in input_file:
        sent_array.append([row[0],row[1]])
        
with open('political_data.csv', 'rb') as polfile:
    input_file = csv.reader(polfile)
    for row in input_file:
        pol_array.append([row[0],[float(row[1]),float(row[2])]])
        
last_user = sent_array[0][0]
first_time = True

#do some prepending, need two different lists here, can do both in the same array
for row in sent_array:
    current_user = row[0]
    if last_user == current_user:
        if first_time:
            user_sent_first_only.append([current_user,row[1],pol_array[0][1]])
            #add to count
            if row[1] == 1:
                clinton+=1
            else:
                trump+=1
            first_time = False
        else:
            #add to count
            if float(row[1]) == 1:
                clinton+=1
            else:
                trump+=1
            last_user = current_user
    else:
       #start new user
       #first total the old stuff and compile it into one sheet
       user_sent_averaged.append([last_user,clinton/(trump+clinton),[s[1] for s in pol_array if s[0]==last_user][0]])
       clinton = trump = 0
       user_sent_first_only.append([current_user,row[1],[s[1] for s in pol_array if s[0]==current_user][0]])
       #add to count
       if float(row[1]) == 1:
           clinton+=1
       else:
           trump+=1
       last_user = current_user
       
#have to append the last user
user_sent_averaged.append([current_user,row[1],[s[1] for s in pol_array if s[0]==current_user][0]])

#save to file
outfile = 'combined_data.csv'
with open(outfile, 'wb') as csvfile:
    writer = csv.writer(csvfile,  quoting=csv.QUOTE_ALL)
    for item in range(0,len(user_sent_averaged)):
        #Write item to outcsv
        writer.writerow([user_sent_averaged[item][0],user_sent_first_only[item][0],
        user_sent_averaged[item][1],user_sent_first_only[item][1],user_sent_averaged[item][2],
        user_sent_first_only[item][2]])
