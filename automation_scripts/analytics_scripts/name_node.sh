#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install -y wget ssh unzip openjdk-8-jdk python3-pip mysql-client-core-5.7
pip3 install --upgrade pip
pip3 install pyspark numpy
#sudo sysctl vm.swappiness=10
echo -e "\n"|ssh-keygen -t rsa -N ""
cat .ssh/id_rsa.pub >> .ssh/authorized_keys
wget https://apachemirror.sg.wuchna.com/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz
tar zxvf hadoop-3.3.0.tar.gz
export JH="\/usr\/lib\/jvm\/java-8-openjdk-amd64"
sed -i "s/# export JAVA_HOME=.*/export\ JAVA_HOME=${JH}/g" hadoop-3.3.0/etc/hadoop/hadoop-env.sh
wget https://apachemirror.sg.wuchna.com/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz
tar zxvf spark-3.0.1-bin-hadoop3.2.tgz
#wget https://apachemirror.sg.wuchna.com/zeppelin/zeppelin-0.9.0-preview2/zeppelin-0.9.0-preview2-bin-all.tgz
#tar zxvf zeppelin-0.9.0-preview2-bin-all.tgz
#wget https://apachemirror.sg.wuchna.com/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz
#tar zxvf sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz
#cp sqoop-1.4.7.bin__hadoop-2.6.0/conf/sqoop-env-template.sh sqoop-1.4.7.bin__hadoop-2.6.0/conf/sqoop-env.sh
#export HD="\/opt\/hadoop-3.3.0"
#sed -i "s/#export HADOOP_COMMON_HOME=.*/export HADOOP_COMMON_HOME=${HD}/g" sqoop-1.4.7.bin__hadoop-2.6.0/conf/sqoop-env.sh
#sed -i "s/#export HADOOP_MAPRED_HOME=.*/export HADOOP_MAPRED_HOME=${HD}/g" sqoop-1.4.7.bin__hadoop-2.6.0/conf/sqoop-env.sh
#wget https://repo1.maven.org/maven2/commons-lang/commons-lang/2.6/commons-lang-2.6.jar
#cp commons-lang-2.6.jar sqoop-1.4.7.bin__hadoop-2.6.0/lib/
#sudo cp -rf sqoop-1.4.7.bin__hadoop-2.6.0 /opt/sqoop-1.4.7
#sudo apt install libmysql-java
#sudo ln -snvf /usr/share/java/mysql-connector-java.jar /opt/sqoop-1.4.7/lib/mysql-connector-java.jar