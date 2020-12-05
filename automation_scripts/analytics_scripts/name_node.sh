#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install -y wget ssh unzip openjdk-8-jdk python3-pip mysql-client-core-5.7 mongodb-clients
pip3 install --upgrade pip
pip3 install pyspark numpy
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
#sudo sysctl vm.swappiness=10
echo -e "\n"|ssh-keygen -t rsa -N ""
cat .ssh/id_rsa.pub >> .ssh/authorized_keys
wget https://apachemirror.sg.wuchna.com/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz
tar zxvf hadoop-3.3.0.tar.gz
export JH="\/usr\/lib\/jvm\/java-8-openjdk-amd64"
sed -i "s/# export JAVA_HOME=.*/export\ JAVA_HOME=${JH}/g" hadoop-3.3.0/etc/hadoop/hadoop-env.sh
wget https://apachemirror.sg.wuchna.com/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz
tar zxvf spark-3.0.1-bin-hadoop3.2.tgz