#  Script to run FindUniqueIds.py
#  Written by Vanessa Job, October 22, 2016

# Delete the finduniqueids.csv directory from the last time you ran the program. 
hdfs dfs -ls hereareuniqueids.csv/*
hdfs dfs -rm hereareuniqueids.csv/*
hdfs dfs -ls hereareuniqueids.csv
hdfs dfs -rmdir hereareuniqueids.csv

# Run FindUniqueIds.py
/usr/bin/spark-submit FindUniqueIds.py 

echo "You can find the unique ids in your hdfs." 
hdfs dfs -ls hereareuniqueids.csv
