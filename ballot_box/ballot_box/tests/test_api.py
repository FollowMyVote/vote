import unittest
import time
from pprint import pprint
from datetime import date, datetime
from ballot_box.modules import api
from ballot_box import settings

class TestAPI(unittest.TestCase):

    def setUp(self):
        api.wallet_open(settings.WALLET_NAME)
        api.wallet_unlock(99999999, settings.WALLET_PASSWORD)
        
    
    def tearDown(self):
        """call after every test case."""

    def get_contest_id(self):
        return api.ballot_get_contests_by_tag('region', 'STATE')['result'][0]
    
  
    def test_api_ballot_get_contests_by_tag(self):
        response = api.ballot_get_contests_by_tag('region', 'STATE')
        print(response)
        self.assertFalse("error" in response);
        self.assertIsNotNone(response['result'])

    def test_api_ballot_get_contest_by_id(self):
        response = api.ballot_get_contest_by_id(self.get_contest_id())
        print(response)
        self.assertFalse("error" in response);
        self.assertIsNotNone(response['result'])

    def test_api_ballot_get_decisions_by_contest(self):
        response = api.ballot_get_decisions_by_contest(self.get_contest_id())
        print(response)
        self.assertFalse("error" in response);
        self.assertIsNotNone(response['result'])

        



if __name__ == "__main__":
    unittest.main()

    
    