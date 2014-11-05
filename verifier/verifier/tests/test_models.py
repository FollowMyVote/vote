import unittest
from pprint import pprint
from verifier.models import Identity





class TestModels(unittest.TestCase):

    def test_get_properties_from_array(self):
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


    def test_identity(self):
        blank_identity = Identity()
        self.assertEquals(blank_identity.id, 0)
        
        dict = {u'id_front_photo': u'IDFronttest0589248',
		        u'id': 1415205896255288L,
		        u'id_back_photo': u'IDBacktest0589248',
		        u'owner': u'XTS3YUrZaG3TAtwRQVqrDGN6AVH8k9goJSZC',
		        u'voter_reg_photo': u'VoterRegtest0589248',
		        u'properties': [{
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
		        }],
		        u'owner_photo': u'OwnerPhototest0589248'
	        }
            
        identity = Identity(dict)
        self.assertIsNotNone(identity.properties)
        
        self.assertEquals(identity.id, 1415205896255288L)
        
        self.assertEquals(identity.id_back_photo, 'IDBacktest0589248')

        self.assertEquals(identity.properties[0].name, 'FirstName')

        


    
        
        

    



 

if __name__ == "__main__":
    unittest.main()

    
    