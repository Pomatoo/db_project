#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install libmysqlclient-dev python3-pip git python3-venv -y
git clone "https://github.com/Pomatoo/db_project.git"
python3 -m venv ~/db_project/flask-app/venv
source ~/db_project/flask-app/venv/bin/activate
pip3 install --upgrade pip
pip3 install mysqlclient PyMySQL pymongo boto3 Flask Flask-WTF Flask-Bcrypt Flask-Login Flask-PyMongo Flask-SQLAlchemy fabric WTForms