#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install -y wget unzip openjdk-8-jdk
sudo sysctl vm.swappiness=10