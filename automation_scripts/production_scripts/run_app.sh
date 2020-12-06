#!/usr/bin/env bash
source ~/flask-web/venv/bin/activate
nohup python3 ~/flask-web/flask-app/run.py deploy > /dev/null 2>&1 &