import csv
import pandas as pd

#use pandas to combine our two files on their UID's
sent = pd.read_csv('out.csv')
sent['sum'] = sent.groupby(['user'])['sentiment'].transform('sum')
sent['ct'] = sent.groupby(['user'])['sentiment'].transform('count')
sent['mean'] = sent['sum']/sent['ct']
sent = sent.sort_values(by ='user' )

passion = pd.read_csv('political_data.csv')
passion = passion.sort_values(by ='user' )
merged = passion.merge(sent, on = 'user')
#convert the merged DataFrame to a list that's python iterable
merged = merged.drop(merged[merged['p'] == 0].index)
f_o = merged.drop_duplicates(subset='user', keep='first')
user_sent_first_only = f_o.values.tolist()
f_l = merged.drop_duplicates(subset='user', keep='first')
full_list = f_l.values.tolist()

#user_sent_averaged = []
#clinton = trump = 0
#last_user = full_list[0][0]
##do some prepending, need two different lists here, can do both in the same array
#for row in range(0,len(full_list)):
#    current_user = int(full_list[row][0])
#    if last_user == current_user:
#        #add to count
#        if full_list[row][3] == 1:
#            clinton+=1
#        else:
#            trump+=1
#        last_user = current_user
#    else:
#       #start new user
#       #first total the old stuff and compile it into one sheet
#       user_sent_averaged.append([full_list[row-1][0],full_list[row-1][1],full_list[row-1][2],float(clinton/(trump+clinton))])
#       clinton = trump = 0
#       #add to count
#       if full_list[row][3] == 1:
#           clinton+=1
#       else:
#           trump+=1
#       last_user = int(current_user)
#       
##save to file
#outfile = 'combined_data2.csv'
#with open(outfile, 'wb') as csvfile:
#    writer = csv.writer(csvfile,  quoting=csv.QUOTE_ALL)
#    for item in range(0,len(user_sent_averaged)):
#        #Write item to outcsv
#        writer.writerow([user_sent_averaged[item][0],user_sent_first_only[item][0],
#        [user_sent_averaged[item][1],user_sent_averaged[item][2]],
#        [user_sent_first_only[item][1],user_sent_first_only[item][2]],
#        user_sent_averaged[item][3],user_sent_first_only[item][3]])

outfile = 'combined_data3.csv'
with open(outfile, 'wb') as csvfile:
    writer = csv.writer(csvfile,  quoting=csv.QUOTE_ALL)
    for item in range(0,len(full_list)):
        #Write item to outcsv
        writer.writerow([full_list[item][0],full_list[item][1],full_list[item][2],full_list[item][3],full_list[item][6],])
