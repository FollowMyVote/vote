import unittest

from verifier import settings
from verifier.data.demo_repository import DemoRepository




class TestRepository(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.db = DemoRepository(settings.DB_TEST_CONNECTION_STRING)

    def tearDown(self):
        self.db.end_session

    def test_get_ballots(self):
        result = self.db.get_ballots()
        print(result)
        self.assertTrue( len(result) > 0)





if __name__ == "__main__":
    unittest.main()