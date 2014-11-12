import requests
import json
import time
import os
import random
import base64
from verifier import settings
from verifier.modules.helpers import log
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

def take_next_request():
    """Gets the next pending request and sets it to be in processing"""
    return make_request({"method": "verifier_take_next_request" ,
           "params": [],
           "jsonrpc": "2.0",
           "id": 0,})

def wallet_account_create(name):
    """creates a new account, mostly used for testing purposes"""
    return make_request({"method": "wallet_account_create" ,
           "params": [name],
           "jsonrpc": "2.0",
           "id": 0,})

def verifier_peek_request(id):
    """gets the specified request does not set any status"""
    return make_request({"method": "verifier_peek_request" ,
           "params": [id],
           "jsonrpc": "2.0",
           "id": 0,})

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

def verifier_list_requests(status="awaiting_processing"):
    """lists requests by status
    
    Statuses:
    awaiting_processing
    in_processing
    accepted:
    rejected
        
    """
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
    """gets a unique account name for creating test accounts"""
    return "test" + str.replace(str(time.time()), ".", "")[-7:]

def get_num_sample_directories():
    """gets the number of sample directories"""
    sample_directories = [x[0] for x in os.walk(settings.APP_SAMPLE_IMAGES)]
    return len(sample_directories) - 1

def get_sample_image(image_name, directory_num):
    """gets a base64 encoded sample image from the sample directory """
    sample_image_path = os.path.join(settings.APP_SAMPLE_IMAGES, 
                                     str(directory_num), image_name)
    sample_image = None
    print (sample_image_path)
    with open(sample_image_path, 'rb') as f:
        sample_image = base64.b64encode(f.read())
    
    print('sample encoded')
    return sample_image


        
    

    

def debug_create_test_request(num_requests):
    """creates a number of test requests   """
    wallet_open(settings.WALLET_NAME)
    wallet_unlock(99999999, settings.WALLET_PASSWORD)
    random.seed()
    last_sample_dir_num = -1
    for i in range(num_requests):
        

        #get sample directory
        #make sure we have a different number than last time for variety
        sample_dir_num = random.randint(1, get_num_sample_directories())
        while sample_dir_num == last_sample_dir_num:
            sample_dir_num = random.randint(1, get_num_sample_directories())

        last_sample_dir_num = sample_dir_num
        debug_create_test_request_from_sample(sample_dir_num)
            

def debug_create_test_request_from_sample(sample_dir_num):
    """creates a test request from the sample directory specified 

    does not open wallet or unlock so beware
    """
    print (sample_dir_num)
    current_name = get_unique_account_name()
    print (current_name)
    pprint(wallet_account_create(current_name))
    pprint(debug_request_verification(current_name,
    get_sample_image('owner.jpg', sample_dir_num),
    get_sample_image('id-front.jpg', sample_dir_num),
    get_sample_image('id-back.jpg', sample_dir_num),
    get_sample_image('voter-card.jpg', sample_dir_num)))

def verifier_resolve_request(request_id, verification_response):
    """opens the specified wallet"""
    return make_request({"method": "verifier_resolve_request" ,
           "params": [request_id, verification_response],
           "jsonrpc": "2.0",
           "id": 0,})




  