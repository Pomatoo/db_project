#!/usr/bin/env bash
mysql -h $MYSQL_HOST -uroot -piStD-So.043-Database -e 'SELECT review_text FROM testDB.review' > reviews.txt
/opt/hadoop-3.3.0/bin/hdfs dfs -rm -r /input
/opt/hadoop-3.3.0/bin/hdfs dfs -mkdir /input
/opt/hadoop-3.3.0/bin/hdfs dfs -put reviews.txt /input
/opt/spark-3.0.1-bin-hadoop3.2/bin/spark-submit --master yarn tfidf.py
/opt/hadoop-3.3.0/bin/hdfs dfs -getmerge /output/tfidf tfidf_result.txt
/opt/hadoop-3.3.0/bin/hdfs dfs -rm -r /input
/opt/hadoop-3.3.0/bin/hdfs dfs -rm -r /output
rm reviews.txt
mv tfidf_result.txt ~/result/tfidf_result_$(date -d "today" +"%Y%m%d%H%M").txt