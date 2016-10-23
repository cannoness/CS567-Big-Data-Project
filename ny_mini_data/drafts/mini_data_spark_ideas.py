
from pyspark import SparkContext, SparkConf
# Need to read file name from file
# Also need to set up usage.

# File must be in hdfs
lines = sc.textFile('project_tests/some.data')
lines.count()
uniquePeople = lines.distinct()
uniquePeople.count()
uniquePeople.collect()
print uniquePeople.collect()

# Need to write uniquePeople to a file.

with open('file.txt', 'a') as f: 
                some_id = json.dumps(data['user']['id_str'])
            	# print json.dumps(data['user']['id_str'])
                print some_id

		f.write (some_id + "\n")
		#f.close()

# What I did with Justin's file.
lines = sc.textFile('project_tests/ids.csv')

# How to separte the csv into lines?

ids = lines.map(lambda line: line.split(","))
ids.count()
