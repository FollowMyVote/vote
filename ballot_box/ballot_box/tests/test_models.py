import unittest
from pprint import pprint
from ballot_box.models import Contest, Contestant
 


class TestContestant(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        dict = {u'name': u'NEEL KASHKARI', 
                u'description': u'Party Preference: Republican\nBusinessman'}

        self.empty  = Contestant()
        self.object = Contestant(dict)

    def test_contestant_empty(self):
        print(self.empty.name)
        self.assertEquals(self.empty.name, '')
    
    def test_contestant_name(self):
        print(self.object.name)
        self.assertEquals(self.object.name, 'NEEL KASHKARI')

    def test_contestant_to_json(self):
        print(self.object.to_json())
        self.object.to_json()

class TestContest(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        d = {
            u'contestants':  
                [{u'name': u'NEEL KASHKARI', u'description': u'Party Preference: Republican\nBusinessman'}, 
                 {u'name': u'EDMUND G. "JERRY" BROWN', u'description': u'Party Preference: Democratic\nGovernor of California'}], 
            u'description': u'', 
            u'tags': 
                [[u'contest type', u'VOTER-NOMINATED'], 
                 [u'name', u'Governor'], 
                 [u'opinion type', u'vote one'], 
                 [u'region', u'STATE']]}

        self.empty  = Contest('ID_empty')
        self.object = Contest('ID', d)

    def test_contest_empty(self):
        self.assertEquals(self.empty.name, '')
    
    def test_contest_name(self):
        print(self.empty.name)
        self.assertEquals(self.object.name, 'Governor')

    def test_contest_tag(self):
        value = self.object.tag('region')
        print(value)
        self.assertEquals(value, 'STATE')
    
    def test_contest_to_json(self):
        print(self.object.to_json())
        self.object.to_json()

    def test_contest_search(self):
        self.assertTrue(self.object.search('NEEL'))
        self.assertTrue(self.object.search('republican'))
        self.assertTrue(self.object.search('STATE'))
        self.assertTrue(self.object.search('vot'))
        self.assertTrue(self.object.search('Governor'))
        self.assertFalse(self.object.search('Governor1'))


if __name__ == "__main__":
    unittest.main()

    
    