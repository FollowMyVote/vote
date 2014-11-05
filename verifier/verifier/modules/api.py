
import requests
import json
import time
from verifier import settings
from verifier.modules.helpers import log
from pprint import pprint, pformat


def make_request(payload):
    """Makes a request using the configuration specified in settings.py, and 
    the payload that has been passed in"""
    log().debug("make_request\n{0}".format(payload))

    response = requests.post(
        settings.API_URL,
        data=json.dumps(payload), 
        headers= {"content-type": "application/json"},
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

def verifier_peek_request(id):
    """creates a new account, mostly used for testing purposes""";
    return make_request({"method": "verifier_peek_request" ,
           "params": [id],
           "jsonrpc": "2.0",
           "id": 0,})

def wallet_open(name):
    """opens the specified wallet""";
    return make_request({"method": "wallet_open" ,
           "params": [name],
           "jsonrpc": "2.0",
           "id": 0,})


def wallet_close():
    """closes the wallet""";
    return make_request({"method": "wallet_close" ,
           "params": [],
           "jsonrpc": "2.0",
           "id": 0,})


def wallet_unlock(timeout, password):
    """unlocks wallet 
    
    timeout is a number for how long it should stay unlocked in seconds
    """;
    return make_request({"method": "wallet_unlock" ,
           "params": [timeout, password],
           "jsonrpc": "2.0",
           "id": 0,})

def verifier_list_requests(status="awaiting_processing"):
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

def debug_request_verification(account_name, owner_photo, id_front_photo, 
                               id_back_photo, voter_reg_photo):
    """creates a new test request"""
    return make_request({"method": "debug_request_verification" ,
           "params": [account_name, 
                      owner_photo, 
                      id_front_photo, 
                      id_back_photo, 
                      voter_reg_photo],
           "jsonrpc": "2.0",
           "id": 0,})

def get_unique_account_name():
    return "test" + str.replace(str(time.time()), ".", "")[-7:]

def debug_create_test_request(num_requests):
    """creates a number of test requests
       
    Wallet must be opened and unlocked before this will work.
    Not sure if there is a way to check the status of the wallet 
    before calling this

    wallet name: default
    wallet password: helloworld
    """
    wallet_open('default')
    wallet_unlock(99999999, 'helloworld')
    

    for i in range(num_requests):
        
        current_name = get_unique_account_name()
        print (current_name)
        pprint(wallet_account_create(current_name))
        pprint(debug_request_verification(
            current_name,
            "Owner Photo {}".format(current_name),
            "ID Front {}".format(current_name),
            "ID Back {}".format(current_name),
            "Voter Reg {0}".format(current_name)))




  