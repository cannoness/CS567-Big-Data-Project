"""SimpleApp.py"""
from pyspark import SparkContext
import csv

logFile = "temp.log"  # Should be some file on your hdfs system.  This is in the home directory of
			# the hdfs

sc = SparkContext("local", "Simple App")   #  What the heck does this mean? 
logData = sc.textFile(logFile).cache()

numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()

#  This actually writes to the directory where SimpleApp.py is being executed.   
with open ('cleaned_output.txt', 'w') as f:
	f.write("Number of a's is " + str(numAs) + ". NumBs is " + str(numBs))


print("\n HEY HEY HEY")
f = open('hey.txt','w')
f.write("Hey!!")
print("\n HEY HEY HEY")
print("\n\n\n")


print "Lines with a: %i, lines with b: %i" % (numAs, numBs)

""" To write a dataset to the hadoop file system, we have to use a Spark context command. """

# Let's try reading in the csv and writing it out to a different file.  

inputFile = sc.textFile('project_tests/ids.csv')
ids = inputFile.flatMap(lambda line: line.split(","))
print "Number of ids in input file is " + str(ids.count())

uniqueIds = ids.distinct()

print "Number of distinct ids is " + str(uniqueIds.count())

print "\n\n\n  Now saving ids to dfs, we hope"
uniqueIds.saveAsTextFile('project_tests/hereareuniqueids.csv')
