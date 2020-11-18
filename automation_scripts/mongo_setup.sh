#!/usr/bin/env bash
sudo apt-get install -y wget
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y unzip mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/meta_kindle_store.zip -O meta_kindle_store.zip
unzip meta_kindle_store.zip
rm -rf meta_kindle_store.zip
mongo <<'EOF'
use admin
db.createUser({ user: "admin",pwd: "iStD-So.043-Database",roles:[{ role: "userAdminAnyDatabase",db: "admin" }, "readWriteAnyDatabase"]})
EOF
mongoimport --db=test --collection=book_meta --file=./meta_Kindle_Store.json --host=localhost --authenticationDatabase admin --username 'admin' --password 'iStD-So.043-Database' --verbose --legacy
sudo chmod 777 /etc/mongod.conf
sudo sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mongod.conf
sudo echo -e 'security:\n  authorization: "enabled"' >> /etc/mongod.conf
sudo systemctl restart mongod