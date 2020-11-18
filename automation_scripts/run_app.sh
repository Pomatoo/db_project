#!/usr/bin/env bash
source ~/db_project/flask-app/venv/bin/activate
nohup python3 ~/db_project/flask-app/run.py deploy > /dev/null 2>&1 &