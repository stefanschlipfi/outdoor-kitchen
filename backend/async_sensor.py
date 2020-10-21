import threading
import psutil
from time import sleep
from datetime import datetime

from utils import *
init_logger(loglevel='DEBUG',filename='async_sensor.log',stream=False,logger_name='sensor')
import logging
logger = logging.getLogger('sensor')

#dht sensor
import Adafruit_DHT


class ThreadSensor(threading.Thread):
    def __init__(self,sensor_dict,DELAY = 5):
        """
        @sensor_dict bus_id / gpio_port, sensor_type
        """
        super().__init__()
        self.DHT_Sensor = Adafruit_DHT.DHT22
        self.DELAY = DELAY
        self.stop_loop = False
        
        self.mongo_db,self.mongo_sensors = mongo_connect()

        if not isinstance(sensor_dict,dict):
            logger.error("sensor_dict musst be a dict")
            raise ValueError("sensor_dict musst be a dict")

        sensor_type = sensor_dict.get('sensor_type')
        gpio_port = sensor_dict.get('gpio_port')
        bus_id = sensor_dict.get('bus_id')

        if sensor_type == None:
            logger.error("sensor_type is required")
            raise Exception("sensor_type is required")
        else:
            self.sensor_type = sensor_type.upper()
            sensor_dict.update({'sensor_type':self.sensor_type})

        if bus_id == None and gpio_port == None:
            logger.error("bus_id or gpio_port is required")
            raise Exception("bus_id or gpio_port is required")
        elif not bus_id == None and not gpio_port == None:
            logger.error("only use bus_id or gpio_port")
            raise Exception("only use bus_id or gpio_port")
        else:
            if not gpio_port == None:
                try:
                    gpio_port = int(gpio_port)
                except:
                    logger.error("gpio_port musst be a int")
                    raise ValueError("gpio_port musst be a int")
                else:
                    self.gpio_port = gpio_port
            elif not bus_id == None:
                self.bus_id = bus_id
        
        self.sensor_dict = sensor_dict.copy()
        self.unchanged_sensor_dict = sensor_dict.copy()

    def load_sensor(self):
        """
        load sensor with attr from sensor_dict
        return new sensor_dict / upated instace sensor_dict
        """
        #remove error if extsts
        try:
            self.sensor_dict.pop("error")
        except:
            pass

        if self.sensor_type == "DHT22":
            self.sensor_dict.update(self.load_dht22(self.gpio_port))
        
        now = datetime.now()
        now_str = '{}-{}-{} {}:{}:{}'.format(now.year,now.month,now.day,now.hour,now.minute,now.second)
        self.sensor_dict.update({'timestamp':now_str})
        return self.sensor_dict
            

    def load_dht22(self,gpio_port):
        """
        @GPIO Port (int)
        read dht22 sensor
        return dict
        """
        try:
            humidity,temp = Adafruit_DHT.read_retry(sensor=self.DHT_Sensor,pin=gpio_port,retries=15)
            if humidity == None and temp == None:
                raise Exception("cannot read gpio_port")
        except Exception as e:
            logger.exception(e)
            logger.error("failed to read data from gpio_port: {}".format(gpio_port))
            return {'humidity':None,'temperature':None,'gpio_port':gpio_port,"error":str(e)}
        else:
            humidity = format(humidity, '.2f')
            temp = format(temp, '.2f')
            logger.debug('GPIO_PORT: {0}, temp: {1}, humidity: {2}'.format(gpio_port,temp,humidity))
            return {'humidity':humidity,'temperature':temp,'gpio_port':gpio_port}

    def get_mongo_itemid(self,sensor_dict):
        """
        get objectid from mongo_sensors (sensor_dict)
        return True,id / False,None
        """
        resp = self.mongo_sensors.find(sensor_dict)
        items = [item for item in resp]
        logger.debug("mongo find resp_count: {}".format(resp.count()))
        if resp.count() == 1:
            logger.debug("found Object_id: {}".format(items[0]['_id']))
            return True,items[0]['_id']
        elif resp.count() == 0:
            logger.debug("no id found in monogodb sensor_dict: {}".format(sensor_dict))
            return False,None
        else:
            for item in items:
                self.mongo_sensors.delete_one(item)
                logger.info("removed item from mongodb, {}".format(str(item)))
            return False,None

    def write_mongo(self,sensor_dict):

        try:
            mongo_id = sensor_dict['_id']
        except:
            self.mongo_sensors.insert(sensor_dict)
            logger.debug("dumped sensor_dict to mongodb")
        else:
            self.mongo_sensors.replace_one({"_id":mongo_id},sensor_dict)
            logger.debug("updated sensor_dict in mongodb id: {}".format(sensor_dict['_id']))
        return True

    def run(self):

        while True:
            self.load_sensor()
            #check if object id is set
            try:
                mongo_id = self.sensor_dict['_id']
            except:
                resp_bool,mongo_id = self.get_mongo_itemid(self.unchanged_sensor_dict)
                if resp_bool:
                    self.sensor_dict.update({'_id':mongo_id})
            finally:
                self.write_mongo(self.sensor_dict)

            if self.stop_loop:
                break
            sleep(self.DELAY)
