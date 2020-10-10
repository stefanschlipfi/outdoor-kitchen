import threading
from utils import *
import psutil

init_logger(loglevel='DEBUG',filename='aysnc_sensor.log',stream=False,logger_name='sensor')
import logging
logger = logging.getLogger('sensor')

#dht sensor
import Adafruit_DHT

class ThreadSensor(threading.Thread):
    def __init__(self,sensor_dict):
        """
        @sensor_dict bus_id / gpio_port, sensor_type
        """
        super().__init__()
        self.DHT_Sensor = Adafruit_DHT.DHT22
        
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
        
        self.sensor_dict = sensor_dict

    def load_sensor(self):
        """
        load sensor with attr from sensor_dict
        return new sensor_dict
        """
        new_sensor_dict = self.sensor_dict
        if self.sensor_type == "DHT22":
            new_sensor_dict.update(self.load_dht22(self.gpio_port))
        return new_sensor_dict
            

    def load_dht22(self,gpio_port):
        """
        @GPIO Port (int)
        read dht22 sensor
        return dict
        """
        try:
            humidity,temp = Adafruit_DHT.read_retry(self.DHT_Sensor,gpio_port)
            if humidity == None and temp == None:
                raise Exception("cannot read gpio_port")
        except Exception as e:
            logger.exception(e)
            logger.error("failed to read data from gpio_port: {}".format(gpio_port))
            return {'humidity':None,'temperature':None,'gpio_port':gpio_port,"error":e}
        else:
            humidity = format(humidity, '.2f')
            temp = format(temp, '.2f')
            logger.debug('GPIO_PORT: {0}, temp: {1}, humidity: {2}'.format(gpio_port,temp,humidity))
            return {'humidity':humidity,'temperature':temp,'gpio_port':gpio_port}

