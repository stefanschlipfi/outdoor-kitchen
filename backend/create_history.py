from utils import *
from threading import Thread
from time import sleep
from datetime import datetime

init_logger(loglevel='DEBUG',filename='histroy_sensor.log',stream=False,logger_name='history_sensor')
import logging
logger = logging.getLogger('history_sensor')


class History(Thread):
    def __init__(self):
        super().__init__()
        self.mongo_db,self.mongo_sensors = mongo_connect()
        self.mongo_history = self.mongo_db['sensor_history']

    def today(self):
        return str(datetime.today().date())
        #today_dict = {today:[]}


    def get_mongo_itemid(self,today_dict):
        """
        search for mongo id with today_dict
        return item
        """
                
        resp = self.mongo_history.find(today_dict)
        items = [item for item in resp]
        if resp.count() == 1:
            logger.debug("found item today! id: {}".format(items[0]['_id']))
            return True,items[0]
        elif resp.count() == 0:
            logger.debug("no item today found in monogodb sensor_history today: {}".format(today))
            return False,None
        else:
            for item in items:
                self.mongo_history.delete_one(item)
                logger.info("removed item from mongodb, {}".format(str(item)))
            return False,None


    def write_today(self,today_item):
        """
        write today item in mongo_sensor_history
        """
        try:
            mongo_id = today_item['_id']
        except:
            self.mongo_history.insert(today_item)
            logger.debug("dumped today_item to mongodb sensor_histroy")
        else:
            self.mongo_history.replace_one({"_id":mongo_id},today_item)
            logger.debug("updated today_item in sensor_histroy id: {}".format(today_item['_id']))
        return True


    def run(self):
        while True:
            sleep(2)
