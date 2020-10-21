#! /bin/bash

source /opt/python-venv/outdoor-kitchen/bin/activate
export FLASK_APP=/opt/outdoor_kitchen/backend/flask_app.py

export PATH=$PATH:/opt/outdoor_kitchen/backend
flask run --host 127.0.0.1 --port=8080
