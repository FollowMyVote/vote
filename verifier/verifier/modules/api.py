
import requests
import json
from verifier import settings
from verifier.modules.helpers import log
from pprint import pprint, pformat

def make_request(payload):
    """Makes a request using the configuration specified in settings.py, and the payload that has been passed in"""
    log().debug('make_request\n%s', pformat(payload))

    response = requests.post(
        settings.API_URL,
        data=json.dumps(payload), 
        headers= {'content-type': 'application/json'},
        auth=(settings.API_USER, settings.API_PASS)).json()

    return response

def take_next_request():
    """Gets the next pending request and sets it to be in processing"""
    return make_request({"method": "verifier_take_next_request" ,
           "params": [],
           "jsonrpc": "2.0",
           "id": 0,})

def wallet_account_create(name):
    """creates a new account, mostly used for testing purposes""";
    return make_request({"method": "wallet_account_create" ,
           "params": [name],
           "jsonrpc": "2.0",
           "id": 0,})

def verifier_list_requests(status):
    """lists requests by status
    
    Statuses:
    awaiting_processing
    in_processing
    accepted:
    rejected
        
    """;
    return make_request({"method": "verifier_list_requests" ,
           "params": [status],
           "jsonrpc": "2.0",
           "id": 0,})

def debug_request_verification(account_name, owner_photo, id_front_photo, id_back_photo, voter_reg_photo):
    """creates a new test request"""
    return make_request({"method": "debug_request_verification" ,
           "params": [account_name, owner_photo, id_front_photo, id_back_photo, voter_reg_photo],
           "jsonrpc": "2.0",
           "id": 0,})





  