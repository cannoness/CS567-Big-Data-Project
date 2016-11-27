from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes   
import csv
sc = SparkContext()
training_set = []

with open('trainingdata.csv', 'rb') as csvfile:
    input_file = csv.reader(csvfile)
    for row in input_file:
        training_set.append(
            {'text': row[1], 'label': row[0]})

training_raw = sc.parallelize(training_set)

# Split data into labels and features, transform
# preservesPartitioning is not really required
# since map without partitioner shouldn't trigger repartitiong
labels = training_raw.map(
    lambda doc: doc['label'],  # Standard Python dict access 
    preservesPartitioning=True # This is obsolete.
    )

tf = HashingTF(numFeatures=100).transform( ## Use much larger number in practice
    training_raw.map(lambda doc: doc['text'].split(), 
    preservesPartitioning=True))

idf = IDF().fit(tf)
tfidf = idf.transform(tf)

# Combine using zip
training = labels.zip(tfidf).map(lambda x: LabeledPoint(x[0], x[1]))

# Train and check
model = NaiveBayes.train(training)
labels_and_preds = labels.zip(model.predict(tfidf)).map(
    lambda x: {"actual": x[0], "predicted": float(x[1])})
print '\n\n\n\n\n\n\n\n\n\n\n\n\n'
print labels_and_preds.collect()
