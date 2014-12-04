import unittest

from verifier import settings, log
from verifier.modules import api
import logging
from verifier.data.demo_repository import DemoRepository




class TestRepository(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.db = DemoRepository(settings.DB_TEST_CONNECTION_STRING)
        #self.db = DemoRepository(settings.DB_CONNECTION_STRING)
        log.setLevel(logging.DEBUG)

    def tearDown(self):
        self.db.end_session

    def test_get_ballots(self):
        result = self.db.get_ballots()
        print(result)
        self.assertTrue( len(result) > 0)

    def test_search_voters(self):
        result = self.db.search_voters(['jones'])
        print(result)
        self.assertTrue(len(result) > 0)

        result = self.db.search_voters(['jones', 'ellen'])

        print(result)
        self.assertTrue(len(result) == 1)

    def test_get_identities(self):
        api.debug_create_test_request(1)
        result = self.db.get_identities()
        print(result)
        self.assertTrue(len(result) > 0)


    def test_get_identity(self):
        api.debug_create_test_request(1)
        result = api.verifier_list_requests()
        id = self.db.get_identity(result['result'][0]['id'])
        print(id)
        self.assertIsNotNone(id)













if __name__ == "__main__":
    unittest.main()