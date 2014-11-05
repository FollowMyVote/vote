from verifier import settings
import logging
import logging.handlers

def setup_logging():
    """sets up logging for the app using config values from settings.py"""

    
    logger = log()
    logger.setLevel(logging.DEBUG)    


    fh = logging.handlers.TimedRotatingFileHandler("verfier.log", "D", 1)
    fh.setLevel(settings.LOG_LEVEL_FILE)
  

    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL_CONSOLE)

    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - "
                                  "%(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.debug("setup_logging complete")
   

def log():
    """returns an instance of the logger for this app"""
    return logging.getLogger("app_log")
    
