import logging
import logging.handlers
import os
from flask import Markup
from datetime import datetime


def setup_logging(log_path= '',  
                  log_file_name='error.log', 
                  file_log_level= logging.ERROR, 
                  console_log_level = logging.ERROR ):
    """sets up logging for the app using config values from settings.py"""

    
    logger = log()
    logger.setLevel(logging.DEBUG)    


    fh = logging.handlers.TimedRotatingFileHandler(os.path.join(log_path, log_file_name ), "D", 1, 60)
    fh.setLevel(file_log_level)
  

    ch = logging.StreamHandler()
    ch.setLevel(console_log_level)

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


def get_cache(cache, key, get_default, timeout = 300):
    """This is a function to help get items from cache 
    
    It will check the cache for the item, if it is not found
    it will execute get_defualt and get the item, and add it to the cache
    
    cache must derive from werkzeug.contrib.cache
    timeout is the number of seconds to keep the object in cache
    """
    value = cache.get(key)
    if value == None:
        value = get_default()
        cache.set(key, value, timeout)

    return value
    




