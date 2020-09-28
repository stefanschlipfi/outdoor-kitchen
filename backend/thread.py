from threading import Thread
from sensor import get_temperature
from time import sleep

from utils import *
init_logger(filename='thread.log',logger_name='thread')
import logging
logger = logging.getLogger('thread')

class TempThread(Thread):
    def __init__(self,socketio,namespace):
        self.delay = 1
        self.socketio = socketio
        self.namespace = namespace
        super().__init__()

    def get_sensors(self):
        """
        Get temperature from sensor.py
        """
        logger.info("Entered infinity loop, delay: {}".format(self.delay))
        while True:
            
            temp_dict = get_sensors()
            self.socketio.emit('server temperature',temp_dict,namespace = self.namespace)
            sleep(self.delay)

    def run(self):
        self.get_sensors()