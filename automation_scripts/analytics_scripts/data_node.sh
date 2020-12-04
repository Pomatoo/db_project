#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install -y wget unzip openjdk-8-jdk
sudo sysctl vm.swappiness=10
tar zxvf hadoop-3.3.0.tgz
sudo mv hadoop-3.3.0 /opt/
sudo mkdir -p /mnt/hadoop/datanode/
sudo chown -R ubuntu:ubuntu /mnt/hadoop/datanode/
tar zxvf spark-3.0.1-bin-hadoop3.2.tgz
sudo mv spark-3.0.1-bin-hadoop3.2 /opt/
sudo chown -R ubuntu:ubuntu /opt/spark-3.0.1-bin-hadoop3.2
rm *gz