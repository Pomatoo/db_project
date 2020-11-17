#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3-pip git python-virtualenv -y

git clone "https://github.com/Pomatoo/db_project.git"
cd db_project/flask-app
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements
python3 run.py


