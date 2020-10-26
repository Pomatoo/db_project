#!/bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install mysql-server wget unzip

wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/kindle-reviews.zip -O kindle-reviews.zip
unzip kindle-reviews.zip
rm -rf kindle_reviews.json kindle-reviews.zip


mysql -uroot <<MYSQL_SCRIPT
CREATE USER 'root'@'%' IDENTIFIED BY 'iStD-So.043-Database';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
CREATE TABLE reviews(
`id` INT(11) NOT NULL AUTO_INCREMENT,
`asin` VARCHAR(255) NOT NULL,
`helpful` VARCHAR(255) NOT NULL,
`overall` VARCHAR(255) NOT NULL,
`review_text` TEXT NOT NULL,
`review_time` VARCHAR(255) NOT NULL,
`reviewer_id` VARCHAR(255) NOT NULL,
`reviewer_name` VARCHAR(255) NOT NULL,
`summary` TEXT NOT NULL,
`unix_review_time` INT(11) NOT NULL,
PRIMARY KEY (`id`),
INDEX idx_asin (asin)
);
LOAD DATA LOCAL INFILE 'kindle_reviews.csv' INTO TABLE reviews FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
MYSQL_SCRIPT

