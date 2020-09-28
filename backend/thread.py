from threading import Thread
from sensor import Sensor
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
        s = Sensor()

        while True:
                
            sensors_dict = s.load_senors()
            self.socketio.emit('sensors',{'sensors_dict':sensors_dict},namespace = self.namespace)
            sleep(self.delay)

    def run(self):
        self.get_sensors()