import unittest

from pprint import pprint
from ballot_box.modules import helpers



class TestHelpers(unittest.TestCase):

    def  test_helpers_get_value(self):
        x = {"test":1}
        
        self.assertEqual(helpers.get_value(x, "test", "default"), 1)

        self.assertEqual(helpers.get_value(x, "test1", "default"), "default")

        self.assertEqual(helpers.get_value(None, "test1", "default"), 
                         "default")

    def test_get_first(self):
        self.assertEqual( helpers.get_first([1, 2]), 1)
        self.assertEqual( helpers.get_first([], 1), 1)
        self.assertEqual( helpers.get_first(None, 1), 1)


    def test_helpers_date_str_to_iso(self):
        self.assertEqual(helpers.date_str_to_iso('12/1/2014'), 
                         '2014-12-01T00:00:00')
        self.assertEqual(helpers.date_str_to_iso('1/28/2014'), 
                         '2014-01-28T00:00:00')

    def test_helpers_iif(self):
        self.assertEqual(helpers.iif(True, 'true', 'false'), 'true')
        self.assertEqual(helpers.iif(False, 'true', 'false'), 'false')
        self.assertEqual(helpers.iif(None, 'true', 'false'), 'false')

    
 

if __name__ == "__main__":
    unittest.main()

    
    