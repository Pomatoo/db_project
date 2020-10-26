import pymysql
import csv
import datetime

print(datetime.datetime.now())
conn = pymysql.connect('localhost', user="root", passwd="1234")
# conn = pymysql.connect('130.211.235.92', user="root", passwd="Wrn3h7^`")

cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS testDB DEFAULT CHARSET utf8 COLLATE utf8_general_ci;')

conn.select_db('testDB')

cursor.execute('drop table if exists user')

sql = """CREATE TABLE IF NOT EXISTS `review` (\
	  `id` int(11) NOT NULL AUTO_INCREMENT,\
	  `asin` varchar(255) NOT NULL,\
	  `helpful` varchar(255) ,\
	  `overall` varchar(255) ,\
	  `review_text` text ,\
	  `review_time` varchar(255) ,\
	  `reviewer_id` varchar(255) NOT NULL,\
	  `reviewer_name` varchar(255) ,\
	  `summary` varchar(1000) ,\
	  `unix_review_time` int(11) NOT NULL,\
	  PRIMARY KEY (`id`),\
	  INDEX idx_asin (asin)
	) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""

cursor.execute(sql)

with open(r'C:\Users\Tomatoo\Desktop\kindle_reviews.csv', mode='r') as csv_file:
    csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)
    next(csv_reader)
    usersvalues = []
    for row in csv_reader:
        usersvalues.append((row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

    cursor.executemany(
        "insert into review(asin,helpful,overall,review_text, review_time, reviewer_id, reviewer_name, summary,"
        "unix_review_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        usersvalues)

cursor.close()

conn.commit()

conn.close()
print(datetime.datetime.now())

# LOAD DATA LOCAL INFILE 'C:\Users\Tomatoo\Desktop\kindle_reviews.csv' INTO TABLE testdb.review FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
