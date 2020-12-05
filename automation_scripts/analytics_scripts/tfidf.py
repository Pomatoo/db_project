from pyspark.mllib.feature import HashingTF, IDF
from pyspark import SparkContext
"""
Following implementation is based on sample provided by Apache Spark repository
It uses building in method to calculate TF-TDF
https://github.com/apache/spark/blob/master/examples/src/main/python/mllib/tf_idf_example.py
"""
sc = SparkContext("local", "TF-IDF")

# Load documents (one per line).
documents = sc.textFile("hdfs://$NAME_NODE_IP:9000/input/reviews.txt").map(lambda line: line.split(" "))

hashingTF = HashingTF()
tf = hashingTF.transform(documents)

# While applying HashingTF only needs a single pass to the data, applying IDF needs two passes:
# First to compute the IDF vector and second to scale the term frequencies by IDF.
tf.cache()
idf = IDF().fit(tf)
tfidf = idf.transform(tf)

# spark.mllib's IDF implementation provides an option for ignoring terms
# which occur in less than a minimum number of documents.
# In such cases, the IDF for these terms is set to 0.
# This feature can be used by passing the minDocFreq value to the IDF constructor.
idfIgnore = IDF(minDocFreq=2).fit(tf)
tfidfIgnore = idfIgnore.transform(tf)

# save tf-idf
tfidfIgnore.saveAsTextFile('hdfs://$NAME_NODE_IP:9000/output/tfidf')
