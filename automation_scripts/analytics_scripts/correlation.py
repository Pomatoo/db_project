import math
import pyspark
from pyspark.sql.functions import *
from pyspark.sql import SparkSession

sc = pyspark.SparkContext("local", "Pearson Correlation")
spark = SparkSession(sc)

"""
length(object)
Computes the character length of string data or number of bytes of binary data.
The length of character data includes the trailing spaces. The length of binary data
includes binary zeros.
"""

# Reviews => ['asin', 'review_text']
reviews = spark.read.csv("hdfs://$NAME_NODE_IP:9000/input/reviews.csv", header=True, sep=",")
asin_and_avg_review_length = reviews.withColumn("review_text", length(reviews.review_text)) \
    .groupBy("asin")\
    .agg(mean("review_text").alias("review_length"))

# Filter null values
asin_and_avg_review_length = asin_and_avg_review_length.filter(asin_and_avg_review_length.review_length.isNotNull())

# Book meta => {'asin':'', 'price':''}
book_meta = spark.read.json("hdfs://$NAME_NODE_IP:9000/input/book_meta.json")
asin_and_prices = book_meta.select("asin", "price")
# Filter null values
asin_and_prices = asin_and_prices.filter(asin_and_prices.price.isNotNull())

# Merge data by 'asin'
data = asin_and_avg_review_length.join(asin_and_prices, "asin")

data = data.select("price", "review_length")
n = data.count()

# data format => [['1.23', 151.0], ..., ['2.99', 235.5]] ([price, average_length])
data = data.rdd.map(list)

flatdata = data.flatMap(lambda row: (
    ("x", float(row[0])),
    ("y", float(row[1])),
    ("x2", float(row[0]) * float(row[0])),
    ("y2", float(row[1]) * float(row[1])),
    ("xy", float(row[0]) * float(row[1]))))

reduced_data = flatdata.reduceByKey(lambda x, y: x + y).sortByKey().collect()

# Order after sorting [x, x2, xy, y, y2]
x = reduced_data[0][1]
x2 = reduced_data[1][1]
xy = reduced_data[2][1]
y = reduced_data[3][1]
y2 = reduced_data[4][1]

numerator = n * xy - (x * y)
denominator = math.sqrt(n * x2 - (x * x)) * math.sqrt(n * y2 - (y * y))
correlation = numerator / denominator

result = sc.parallelize([correlation])
result.saveAsTextFile("hdfs://$NAME_NODE_IP:9000/output/correlation")

print("The Pearson Correlation is: %s " % correlation)