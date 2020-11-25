#!/usr/bin/env bash
sudo apt-get update
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
LOAD DATA LOCAL INFILE 'kindle_reviews.csv' INTO TABLE testDB.review FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
CREATE TABLE testDB.user(
`id` INT(11) NOT NULL AUTO_INCREMENT,
`user_id` VARCHAR(255),
`username` VARCHAR(255),
`password` VARCHAR(255),
PRIMARY KEY (`id`),
INDEX idx_user_id (user_id)
);
INSERT INTO testDB.`user` (user_id, username)
SELECT DISTINCT reviewer_id, reviewer_name
FROM testDB.review;
UPDATE testDB.`user`
SET password = 'user'
WHERE id=id;
EOF
sudo chmod 777 /etc/mysql/my.cnf
sudo echo "bind-address = 0.0.0.0" >> /etc/alternatives/my.cnf
sudo systemctl restart mysql