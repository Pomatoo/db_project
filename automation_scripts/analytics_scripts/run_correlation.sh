#!/usr/bin/env bash
echo "Getting dataset from MySQL"
mysql -h $MYSQL_HOST -uroot -piStD-So.043-Database -e 'SELECT asin,review_text FROM testDB.review' | sed "s/\t/,/g" > reviews.csv
echo "Getting dataset from MongoDB"
mongoexport --uri=mongodb://admin:iStD-So.043-Database@$MONGO_HOST:27017/test?authSource=admin --collection=book_meta --out=./book_meta.json
/opt/hadoop-3.3.0/bin/hdfs dfs -rm -r /input
/opt/hadoop-3.3.0/bin/hdfs dfs -rm -r /output
/opt/hadoop-3.3.0/bin/hdfs dfs -mkdir /input
/opt/hadoop-3.3.0/bin/hdfs dfs -put reviews.csv /input
/opt/hadoop-3.3.0/bin/hdfs dfs -put book_meta.json /input
echo "Running Correlation Job"
/opt/spark-3.0.1-bin-hadoop3.2/bin/spark-submit --master yarn correlation.py
echo "Merging result of Correlation Job"
/opt/hadoop-3.3.0/bin/hdfs dfs -getmerge /output/correlation correlation_result.txt
/opt/hadoop-3.3.0/bin/hdfs dfs -rm -r /input
/opt/hadoop-3.3.0/bin/hdfs dfs -rm -r /output
rm book_meta.json reviews.csv
mv correlation_result.txt ~/result/correlation_result_$(date -d "today" +"%Y%m%d%H%M").txt
echo "Done!"