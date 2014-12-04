import unittest

from ballot_box.modules import api
from ballot_box import settings


class TestAPI(unittest.TestCase):
    def setUp(self):
        api.wallet_open(settings.WALLET_NAME)
        api.wallet_unlock(99999999, settings.WALLET_PASSWORD)

    def tearDown(self):
        """call after every test case."""

    def get_contest_id(self):
        return api.ballot_list_contests()['result'][0]

    def get_decision_id(self):
        return api.ballot_list_decisions()['result'][0]

    def get_voter_id(self):
        return api.ballot_get_decision(self.get_decision_id())['result']['voter_id']






    def test_api_ballot_get_contests_by_tag(self):
        response = api.ballot_get_contests_by_tag('region', 'State')
        print(response)
        self.assertFalse("error" in response)
        self.assertIsNotNone(response['result'])

    def test_api_ballot_ballot_get_all_contests(self):
        response = api.ballot_get_all_contests()
        print(response)
        self.assertTrue(len(response) > 0)

    def test_api_ballot_get_contest_by_id(self):
        response = api.ballot_get_contest_by_id(self.get_contest_id())
        print(response)
        self.assertFalse("error" in response)
        self.assertIsNotNone(response['result'])

    def test_api_ballot_get_decision_ids_by_contest(self):
        response = api.ballot_get_decisions_ids_by_contest(self.get_contest_id())
        print(response)
        self.assertFalse("error" in response)
        self.assertIsNotNone(response['result'])

    def test_api_ballot_get_decisions_by_contest(self):
        """test get decisions by contest assumes the contest id returned by get_contest_id has some decisions """
        response = api.ballot_get_decisions_by_contest(self.get_contest_id())
        print(response)
        self.assertTrue(len(response) > 0)


    def test_api_ballot_get_decision_by_id(self):

        response = api.ballot_get_decision(self.get_decision_id())
        print(response)
        self.assertFalse("error" in response)
        self.assertIsNotNone(response['result'])

    def test_api_ballot_get_decision_ids_by_voter(self):
        voter_id = self.get_voter_id()
        response = api.ballot_get_decisions_ids_by_voter(voter_id)
        print(response)
        self.assertFalse("error" in response)
        self.assertIsNotNone(response['result'])

    def test_api_ballot_get_decisions_by_voter(self):
        voter_id = self.get_voter_id()
        response = api.ballot_get_decisions_by_voter(voter_id)
        print(response)


if __name__ == "__main__":
    unittest.main()