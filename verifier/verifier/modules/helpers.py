from verifier import app
import logging
import logging.handlers

def setup_logging():
    logger = log()
    logger.setLevel(logging.DEBUG)    


    fh = logging.handlers.TimedRotatingFileHandler('verfier.log', 'D', 1)
    fh.setLevel(app.config["LOG_FILE_LEVEL"])
  

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.debug('setup_logging complete')

def log():
    return logging.getLogger('app_log')
    
