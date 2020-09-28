import logging,json

def load_conf():
    with open('/home/stefan/develop/outdoor-kitchen/conf.json') as json_file:
        json_obj = json.load(json_file)

    return json_obj

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


