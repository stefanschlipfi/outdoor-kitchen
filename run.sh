#! /usr/bin/bash

export FLASK_ENV=/opt/python-venv/outdoor-kitchen/bin/python
export FLASK_APP=./backend/flask_app.py

flask run --host 192.168.1.170 --port=8080
