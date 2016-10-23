"""FindUniqueIds.py"""
""" This program written by Vanessa Job, October 16, 2016"""

"""  
    To run the program, issue the command ./bin/spark-submitspark FindUniqueId.py.
    (You must be in your VM or somewhere where you have pyspark installed.  
    The program creates a directory of unique ids in the directory hereareuniqueids.csv
    which is a subdirectory of your hdfs's homedirectory. 

    Instead of doing all this by hand, you can run the script FindUniqueIds.sh
"""


from pyspark import SparkContext
import csv



sc = SparkContext("local", "Simple App")   #  What the heck does this mean? 

print("\n HEY HEY HEY")
	


# Should be wrapped in something to catch exceptions!
# Read in the input, a csv, and flat map it to remove commas and separate out each id. 
inputFile = sc.textFile('project_tests/ids.csv')
ids = inputFile.flatMap(lambda line: line.split(","))

# Save unique ides in rdd uniqueIds
uniqueIds = ids.distinct()

idsCount = ids.count()
uniqueCount = uniqueIds.count()
print "Number of ids in input file is " + str(idsCount)
print "Number of distinct ids is " + str(uniqueCount)

with open ('log.txt', 'w') as f:
	f.write("Number of ids in input file is " + str(idsCount))
	f.write("Number of distinct ids is "  + str(uniqueCount))


print "\n\n\n  Now saving ids to dfs."

""" 
To write a dataset to the hadoop file system, we have to use a Spark context command. The 
output is a directory that contains the unique ids partitioned into several files.  In our case,
this will be one file.  REMEMBER, this output ends up in the hdfs.   Presently, the directory ends
up as a subdirectory of the home directory.  
"""


uniqueIds.saveAsTextFile('./hereareuniqueids.csv')
