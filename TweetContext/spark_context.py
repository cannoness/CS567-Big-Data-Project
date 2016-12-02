from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes   
import csv

sc = SparkContext()
training_set = []
testing_set = []

with open('trainingdata.csv', 'rb') as csvfile:
    input_file = csv.reader(csvfile)
    for row in input_file:
        training_set.append(
            {'label': row[0], 'text': row[1]})

with open('political_tweet.csv','rb') as csv2file:
    input_file = csv.reader(csv2file)
    for row in input_file:
        testing_set.append(
            {'label': row[0], 'text': row[1]})

training_raw = sc.parallelize(training_set)

# Split data into labels and features, transform
labels = training_raw.map(lambda doc: doc['label'])

tf = HashingTF(numFeatures=6000).transform( 
    training_raw.map(lambda doc: doc['text'].split()))

idf = IDF(minDocFreq=2).fit(tf)
tfidf = idf.transform(tf)

# Combine using zip
training = labels.zip(tfidf).map(lambda x: LabeledPoint(x[0], x[1]))

# Train and check
model = NaiveBayes.train(training)
labels_and_preds = labels.zip(model.predict(tfidf)).map(
    lambda x: {"actual": x[0], "predicted": float(x[1])})
print '\n\n\n\n\n\n\n\n\n\n\n\n\n'
print labels_and_preds.collect()

p1 = sc.parallelize(testing_set)

tf1 = HashingTF(numFeatures=6000).transform(
    p1.map(lambda tweet: tweet['text'].split()))

idf1 = IDF(minDocFreq=2).fit(tf1)
tfidf1 = idf1.transform(tf1)

labels2 = p1.map(lambda doc: doc['label'])

testing = labels2.zip(tfidf1).map(lambda x: LabeledPoint(x[0], x[1]))


#test = model.predict(tfidf1)
test = labels2.zip(model.predict(tfidf1)).map(lambda x: { "user":x[0],"predicted": float(x[1])})


outfile = 'out.csv'
with open(outfile, 'wb') as csvfile:
    writer = csv.writer(csvfile,  quoting=csv.QUOTE_ALL)
    for item in test.collect():
        #Write item to outcsv
        writer.writerow([item['user'],item['predicted']])

print str(test.collect())
print '\n\n\n\n\n\n\n\n\n\n\n\n\n'
