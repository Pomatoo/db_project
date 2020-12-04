#!/usr/bin/env bash
/opt/hadoop-3.3.0/sbin/start-dfs.sh && /opt/hadoop-3.3.0/sbin/start-yarn.sh
/opt/spark-3.0.1-bin-hadoop3.2/sbin/start-all.sh
#mysql -u root -piStD-So.043-Database -h 34.72.136.99 -P 3306<<'EOF'
#SELECT review_text FROM testDB.review INTO OUTFILE './reviews.txt'
#EOF
mysql -h 34.72.136.99 -uroot -piStD-So.043-Database -e 'SELECT review_text FROM testDB.review' > review.txt