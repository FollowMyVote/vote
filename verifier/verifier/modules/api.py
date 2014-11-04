from verifier import app
import requests
import json

def make_request(payload):
    response = requests.post(
        url, 
        data=json.dumps(payload), headers=headers,
        auth=(user, password))
    return response

def take_next_request():
    return make_request({"method": "verifier_take_next_request" ,
           "params": [],
           "jsonrpc": "2.0",
           "id": 0,})

  