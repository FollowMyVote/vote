from verifier import settings
import logging
import os
import logging.handlers
from flask import Markup
from datetime import datetime

def setup_logging():
    """sets up logging for the app using config values from settings.py"""

    
    logger = log()
    logger.setLevel(logging.DEBUG)    


    fh = logging.handlers.TimedRotatingFileHandler(os.path.join(settings.APP_LOGS,"verfier.log"), "D", 1, 60)
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
    

def get_value(dict,  key, default = None):
    """gets a value from a dictonary if it exists, returns default if not"""
    if not dict:
        return default
        
    if key in dict:
        return dict[key]
    else:
        return default

def remove_if_exists(dict, key):
    if key in dict:
        del dict[key]

   
def get_first(list, default=None):
    """gets the first value in a list otherwise returns the default"""
    if list:
        for item in list:
            return item
    return default

def iif(expression, true_value, false_value):
    """inline if function"""
    if expression:
        return true_value
    else:
        return false_value

def alert(message, type="info"):
    """gets an alert box, type values are info, success, warning, danger"""
    return Markup('<div class="alert alert-{0}">{1}</div>'
                  .format(type, message))

def date_str_to_iso(str):
    """converts a date string mm/dd/yyyy into iso string format"""
    return datetime.strptime(str, "%m/%d/%Y").isoformat()