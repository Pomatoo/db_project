#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install -y wget unzip openjdk-8-jdk-headless
wget https://apachemirror.sg.wuchna.com/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz
tar zxvf hadoop-3.3.0.tar.gz
export JH="\/usr\/lib\/jvm\/java-8-openjdk-amd64"
sed -i "s/# export JAVA_HOME=.*/export\ JAVA_HOME=${JH}/g" hadoop-3.3.0/etc/hadoop/hadoop-env.sh
sudo mv hadoop-3.3.0 /opt/
sudo mkdir -p /mnt/hadoop/datanode/
sudo chown -R hadoop:hadoop /mnt/hadoop/datanode/
/opt/hadoop-3.3.0/bin/hdfs namenode -format <<-EOF
y
EOF