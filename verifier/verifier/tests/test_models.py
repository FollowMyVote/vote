import unittest
from pprint import pprint
from verifier.models import Identity, IdentityProperty



class TestIdentityProperty(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        dict = {u'salt': u'234',
			    u'name': u'LastName',
			    u'value': None,
			    u'verifier_signatures': []}
        self.empty_property = IdentityProperty()
        self.property = IdentityProperty(dict)

    def test_identity_property_empty(self):
        self.assertEquals(self.empty_property.name, "")
    
    def test_identity_property_last_name(self):
        self.assertEquals(self.property.name, "LastName")

    def test_identity_property_to_json(self):
        self.property.to_json()






class TestIndentity(unittest.TestCase):


    def setUp(self):
        """Call before every test case."""
        dict = {u'id_front_photo': u'IDFronttest0589248',
                u'id': 1415205896255288L,
                u'id_back_photo': u'IDBacktest0589248',
                u'owner': u'XTS3YUrZaG3TAtwRQVqrDGN6AVH8k9goJSZC',
                u'voter_reg_photo': u'VoterRegtest0589248',
                u'properties': [
                    {
                        u'salt': u'123',
                        u'name': u'FirstName',
                        u'value': u'Test First',
                        u'verifier_signatures': []
                    },
                    {
                        u'salt': u'234',
                        u'name': u'LastName',
                        u'value': None,
                        u'verifier_signatures': []
                    },
                    {
                        u'salt': u'345',
                        u'name': u'SSN',
                        u'value': None,
                        u'verifier_signatures': []
                    }],
                u'owner_photo': u'OwnerPhototest0589248'}
        self.empty_identity = Identity()
        self.identity = Identity(dict)

    def test_identity_get_properties_from_array(self):
        x = [{
		        u'salt': u'123',
		        u'name': u'FirstName',
		        u'value': None,
		        u'verifier_signatures': []
	        },
	        {
		        u'salt': u'234',
		        u'name': u'LastName',
		        u'value': None,
		        u'verifier_signatures': []
	        },
	        {
		        u'salt': u'345',
		        u'name': u'SSN',
		        u'value': None,
		        u'verifier_signatures': []
	        }]

        properties = Identity.get_properties_from_array(x)
        
        self.assertEquals(len(properties), 3)
        self.assertEquals(properties[0].name, "FirstName")

        x = []
        properties = Identity.get_properties_from_array(x)
        self.assertEquals(len(properties), 0)

    def test_identity_empty(self):
        self.assertEquals(self.empty_identity.id, 0)      

    def test_identity_properties(self):
        self.assertIsNotNone(self.identity.properties)
        self.assertEquals(self.identity.properties[0].name, 'FirstName')

    def test_identity_property(self):
        self.assertEquals(self.identity.id_back_photo, 'IDBacktest0589248')

    def test_identity_to_dict(self):
        dict = self.identity.to_dict()
        self.assertIsNotNone(dict)
        self.assertEquals(dict['id_front_photo'], 'IDFronttest0589248')
        self.assertEquals(len(dict['properties']), 3)

    def test_identity_to_json(self):
        self.identity.to_json()
        


    

 

if __name__ == "__main__":
    unittest.main()

    
    