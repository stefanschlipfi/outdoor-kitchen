import threading
from time import sleep

from utils import *
init_logger(filename='mongo_observer.log',logger_name='mongo_observer')
import logging
logger = logging.getLogger('mongo_observer')

class MongoObserver(threading.Thread):

    def __init__(self,find_pattern = {},DELAY = 2,socketio = None,namespace = None):
        super().__init__()
        self.mongo_db,self.mongo_sensors = mongo_connect()
        self.resp_list = None
        self.resp_cursor = None

        self.find_pattern = find_pattern
        self.DELAY = DELAY

        #websocket
        self.socketio = socketio
        self.namespace = namespace

        self.stop_loop = False

    def find(self):
        """
        find entry with instace find_pattern
        """

        self.resp_cursor = self.mongo_sensors.find(self.find_pattern)
        self.resp_list = list()
        for item in self.resp_cursor:
            item['_id'] = str(item['_id'])
            self.resp_list.append(item)

        return self.resp_list,self.resp_cursor

    def emit(self):
        logger.info("emited data to socketio, namespace: {}".format(self.namespace))
        self.socketio.emit('sensors_v2',{'sensors_list':self.resp_list },namespace = self.namespace)

    def run(self):
        
        while True:
            self.find()

            if not self.socketio == None and not self.namespace == None:
                self.emit()
            
            if self.stop_loop:
                    break
            sleep(self.DELAY)