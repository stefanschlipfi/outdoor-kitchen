from utils import *
from async_sensor import ThreadSensor

def load_fromconfig():
    """
    load sensors from json config
    return dict with instances
    """
    
    #clear db
    mongodb,mongo_sensors = mongo_connect()
    mongo_sensors.drop()

    sensors_dict = {}
    sensor_list_config = load_conf()['sensors']
    if not isinstance(sensor_list_config,list):
        raise ValueError("sensor_list_config musst be a list")
    
    for sensor_config in sensor_list_config:
        name = sensor_config.get('name')
    
        if name == None or name in sensors_dict:
            name = str(sensor_config)
    
        try:
            instance = ThreadSensor(sensor_config)
        except Exception as e:
            sensors_dict.update({name:{"sensor_config":sensor_config,"error":str(e)}})
            continue
        else:
            instance.start()
            sensors_dict.update({name:{"sensor_config":sensor_config,"async_sensor_instance":instance}})

    return sensors_dict

if __name__ == "__main__":
    sensors_dict = load_fromconfig()
