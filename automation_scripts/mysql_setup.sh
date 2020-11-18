#!/usr/bin/env bash
sudo apt-get update && sudo apt-get upgrade -y
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password isTdSoo43'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password isTdSoo43'
sudo apt-get -y install mysql-server
sudo apt-get -y install wget unzip
wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/kindle-reviews.zip -O kindle-reviews.zip
unzip kindle-reviews.zip
rm -rf kindle_reviews.json kindle-reviews.zip
sudo systemctl start mysql
sudo mysql -u root -pisTdSoo43<<'EOF'
CREATE USER 'root'@'%' IDENTIFIED BY 'iStD-So.043-Database';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS testDB DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
CREATE TABLE testDB.review(
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
CREATE TABLE testDB.user(
`id` INT(11) NOT NULL AUTO_INCREMENT,
`username` VARCHAR(255) NOT NULL,
`password` VARCHAR(255) NOT NULL,
PRIMARY KEY (`id`),
INDEX idx_username (username)
);
LOAD DATA LOCAL INFILE 'kindle_reviews.csv' INTO TABLE testDB.review FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
EOF
sudo chmod 777 /etc/mysql/my.cnf
sudo echo "bind-address = 0.0.0.0" >> /etc/alternatives/my.cnf
sudo systemctl restart mysql