import logging,json
from pymongo import MongoClient

def load_conf():
    with open('/etc/outdoor-kitchen/conf.json') as json_file:
        json_obj = json.load(json_file)

    return json_obj

def mongo_connect():
    """
    connect to mongodb
    return mongodb and sensors collection
    """
    #mongo client
    mongo_client = MongoClient()
    mongo_db = mongo_client["outdoor-kitchen"]
    mongo_sensors = mongo_db["sensors"]
    return mongo_db,mongo_sensors

def init_logger(loglevel = 'INFO',stream = False,filename='outdoor-kitchen.log',logger_name = 'outdoor-kitchen'):
    loglevel = logging.getLevelName(loglevel.upper())
    if not isinstance(loglevel,int):
        raise TypeError("unknown Logging" + str(loglevel))
    logger = logging.getLogger(logger_name)
    logger.setLevel(loglevel)

    stream_formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(stream_formatter)

    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('/var/python-logs/outdoor-kitchen/' + filename,mode='a')
    fh.setLevel(loglevel)
    fh.setFormatter(file_formatter)

    handlers = [fh]
    if stream:
        handlers.append(ch)

    logger.handlers = handlers


