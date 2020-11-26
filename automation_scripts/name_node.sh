#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install -y wget ssh unzip openjdk-8-jdk
sudo sysctl vm.swappiness=10
wget https://apachemirror.sg.wuchna.com/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz
tar zxvf hadoop-3.3.0.tar.gz
export JH="\/usr\/lib\/jvm\/java-8-openjdk-amd64"
sed -i "s/# export JAVA_HOME=.*/export\ JAVA_HOME=${JH}/g" hadoop-3.3.0/etc/hadoop/hadoop-env.sh
echo -e "\n"|ssh-keygen -t rsa -N ""
cat .ssh/id_rsa.pub >> .ssh/authorized_keys