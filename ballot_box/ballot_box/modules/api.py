import json

import requests
from ballot_box import settings, log



def make_request(payload):
    """Makes a request using the configuration specified in settings.py, and 
    the payload that has been passed in"""

    log.info("make_request\n{0}\n{1}".format(settings.API_URL,
                                               payload['method']))

    log.debug("make_request\n{0}\n{1}".format(settings.API_URL,
                                                json.dumps(payload)))

    response = requests.post(settings.API_URL,
                             data=json.dumps(payload),
                             headers={"content-type": "application/json"},
                             auth=(settings.API_USER, settings.API_PASS))

    log.debug(response.content)
    return response.json()


def wallet_open(name):
    """opens the specified wallet"""
    return make_request({"method": "wallet_open",
                         "params": [name],
                         "jsonrpc": "2.0",
                         "id": 0, })


def wallet_close():
    """closes the wallet"""
    return make_request({"method": "wallet_close",
                         "params": [],
                         "jsonrpc": "2.0",
                         "id": 0, })


def wallet_unlock(timeout, password):
    """unlocks wallet 
    
    timeout is a number for how long it should stay unlocked in seconds
    """
    return make_request({"method": "wallet_unlock",
                         "params": [timeout, password],
                         "jsonrpc": "2.0",
                         "id": 0, })


def ballot_get_contests_by_tag(key, value):
    """Gets the next pending request and sets it to be in processing"""
    return make_request({"method": "ballot_get_contests_by_tag",
                         "params": [key, value],
                         "jsonrpc": "2.0",
                         "id": 0, })


def ballot_get_all_contests():
    """gets all contests, this is temporary but it should work for now  """
    all_contests = []
    result = ballot_list_contests(limit=100000000).get('result')
    if result:
        contests = batch('ballot_get_contest_by_id', [[r] for r in result]).get('result')
        if contests:
            all_contests = contests

    return all_contests


def ballot_get_decision(decision_id):
    """gets decision by id"""
    return make_request({"method": "ballot_get_decision",
                         "params": [decision_id],
                         "jsonrpc": "2.0",
                         "id": 0, })


def ballot_get_contest_by_id(contest_id):
    """gets contest details by contest id"""
    return make_request({"method": "ballot_get_contest_by_id",
                         "params": [contest_id],
                         "jsonrpc": "2.0",
                         "id": 0, })


def ballot_get_tag_values_by_key(key):
    """gets tag values by tag """
    return make_request({"method": "ballot_get_tag_values_by_key",
                         "params": [key],
                         "jsonrpc": "2.0",
                         "id": 0, })


def ballot_get_decisions_ids_by_contest(contest_id):
    """gets decision ids by contest"""
    return make_request({"method": "ballot_get_decisions_by_contest",
                         "params": [contest_id],
                         "jsonrpc": "2.0",
                         "id": 0, })


def ballot_get_decisions_by_contest(contest_id):
    """gets all contests, this is temporary but it should work for now  """
    decisions = []
    result = ballot_get_decisions_ids_by_contest(contest_id).get('result')
    if result:
        decisions = batch('ballot_get_decision', [[r] for r in result]).get('result')

    return decisions if decisions else []

def ballot_list_contests(skip_until_id=0, limit=10):
    """gets contest ids """
    return make_request({"method": "ballot_list_contests",
                         "params": [skip_until_id, limit],
                         "jsonrpc": "2.0",
                         "id": 0, })

def ballot_list_decisions(skip_until_id=0, limit=10):
    """gets decision id;s"""
    return make_request({"method": "ballot_list_decisions",
                         "params": [skip_until_id, limit],
                         "jsonrpc": "2.0",
                         "id": 0, })

def ballot_list_ballots(skip_until_id=0, limit=10):
    """gets decision id;s"""
    return make_request({"method": "ballot_list_ballots",
                         "params": [skip_until_id, limit],
                         "jsonrpc": "2.0",
                         "id": 0, })


def batch(method_name, parameters_list=None):
    """gets decision id;s"""

    if not parameters_list:
        parameters_list = []

    return make_request({"method": "batch",
                         "params": [method_name, parameters_list],
                         "jsonrpc": "2.0",
                         "id": 0, })


