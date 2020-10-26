#!/bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install mongodb-org wget unzip -y

sudo systemctl enable mongod
sudo service mongod start

wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/meta_kindle_store.zip -O meta_kindle_store.zip
unzip meta_kindle_store.zip
rm -rf meta_kindle_store.zip

