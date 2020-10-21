from flask import Flask,render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = 'JdeEVd0uzGzjRxTC$DM2LKy!'

import sys
sys.path.append('/opt/outdoor_kitchen/backend')

#websocket
from flask_socketio import SocketIO, emit
socketio = SocketIO(app,cors_allowed_origins='*',async_mode="threading")

#import logger
from utils import *
logger_name = 'flask_views'
init_logger(loglevel='DEBUG',filename='flask_views.log',logger_name=logger_name)
import logging
logger = logging.getLogger(logger_name)

#import CPU Thread from thread.py
from thread import TempThread
from mongo_observer import MongoObserver

#Websocket old Way
@app.route('/old/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/ws_sensors')
def test_connect():
    logger.debug("Connected with socket.io")
    thread = TempThread(socketio=socketio,namespace='/ws_sensors')
    thread.start()

@socketio.on('disconnect', namespace='/ws_sensors')
def test_disconnect():
    logger.debug("Client disconnected")

#Websocket new backend way (mongodb)
@app.route('/')
def index_v2():
    return render_template('index_v2.html')

@socketio.on('connect', namespace='/ws_sensors_v2')
def connect():
    logger.debug("Connected with socket.io")
    thread = MongoObserver(socketio=socketio,namespace='/ws_sensors_v2')
    thread.start()

@socketio.on('disconnect', namespace='/ws_sensors_v2')
def disconnect():
    logger.debug("Client disconnected")


if __name__ == "__main__":
   
    import eventlet
    eventlet.monkey_patch()

    socketio.run(app)

    
