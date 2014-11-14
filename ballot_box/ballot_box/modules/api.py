import requests
import json
import time
import os
import random
import base64
from ballot_box import settings
from ballot_box.modules.helpers import log
from pprint import pprint, pformat



def make_request(payload):
    """Makes a request using the configuration specified in settings.py, and 
    the payload that has been passed in"""

    log().info("make_request\n{0}\n{1}".format(settings.API_URL, 
                                               payload['method']))

    log().debug("make_request\n{0}\n{1}".format(settings.API_URL, 
                                               json.dumps(payload)))
    
    response = requests.post(settings.API_URL,
        data=json.dumps(payload), 
        headers= {"content-type": "application/json"},
        auth=(settings.API_USER, settings.API_PASS))

    log().debug(response.content)
    return response.json()


def wallet_open(name):
    """opens the specified wallet"""
    return make_request({"method": "wallet_open" ,
           "params": [name],
           "jsonrpc": "2.0",
           "id": 0,})


def wallet_close():
    """closes the wallet"""
    return make_request({"method": "wallet_close" ,
           "params": [],
           "jsonrpc": "2.0",
           "id": 0,})


def wallet_unlock(timeout, password):
    """unlocks wallet 
    
    timeout is a number for how long it should stay unlocked in seconds
    """
    return make_request({"method": "wallet_unlock" ,
           "params": [timeout, password],
           "jsonrpc": "2.0",
           "id": 0,})


def ballot_get_contests_by_tag(key, value):
    """Gets the next pending request and sets it to be in processing"""
    return make_request({"method": "ballot_get_contests_by_tag" ,
           "params": [key, value],
           "jsonrpc": "2.0",
           "id": 0,})


def ballot_get_contest_by_id(contest_id):
    """Gets the next pending request and sets it to be in processing"""
    return make_request({"method": "ballot_get_contest_by_id" ,
           "params": [contest_id],
           "jsonrpc": "2.0",
           "id": 0,})


def ballot_get_tag_values_by_key(key):
    """Gets the next pending request and sets it to be in processing"""
    return make_request({"method": "ballot_get_tag_values_by_key" ,
           "params": [key],
           "jsonrpc": "2.0",
           "id": 0,})

def ballot_get_decisions_by_contest(contest_id):
    """Gets the next pending request and sets it to be in processing"""
    return make_request({"method": "ballot_get_decisions_by_contest" ,
           "params": [contest_id],
           "jsonrpc": "2.0",
           "id": 0,})





  