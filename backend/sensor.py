from utils import *
import psutil

init_logger(loglevel='DEBUG',filename='sensor.log',stream=False,logger_name='sensor')
import logging
logger = logging.getLogger('sensor')

#dht sensor
import Adafruit_DHT

class Sensor():
    def __init__(self):
        self.DHT_Sensor = Adafruit_DHT.DHT22
        self.config = load_conf()['sensors']

    def load_senors(self):
        """
        load sensors from config
        return dict
        """
        device_dict = {}

        for sensor_type,sensor_list in self.config.items():
            if sensor_type == 'DHT22':
                dht_dict = device_dict.get('DHT22')
                if not dht_dict:
                    dht_dict = {}

                for sensor in sensor_list:
                    sensor_dict = self.load_dht22(sensor["gpio_port"])
                    sensor_dict.update({'name':sensor["name"]})
                    dht_dict.update({sensor["name"]:sensor_dict})
                device_dict.update({'DHT22':dht_dict})

        return device_dict


    def load_dht22(self,gpio_port):
        """
        @GPIO Port (int)
        read dht22 sensor
        return dict
        """
        humidity,temp = Adafruit_DHT.read_retry(self.DHT_Sensor,gpio_port)
        humidity = format(humidity, '.2f')
        temp = format(temp, '.2f')
        logger.debug('GPIO_PORT: {0}, temp: {1}, humidity: {2}'.format(gpio_port,temp,humidity))
        return {'humidity':humidity,'temperature':temp,'gpio_port':gpio_port}
