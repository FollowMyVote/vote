import json
from verifier.modules import helpers

class IdentityProperty:
    """property value for identity properties"""
    
    def __init__(self, dict = {}):
        """initialize an identity property"""
        self.salt = helpers.get_value(dict, 'salt', '')
        self.name = helpers.get_value(dict, 'name', '')
        self.value = helpers.get_value(dict, 'value', None)
        self.verifier_signatures = helpers.get_value(dict, 'verifier_signatures', [])
        

    def __repr__(self):
        return self.to_json()
       
    def to_json(self):
        """convert object to json string"""
        return json.dumps(self.__dict__)



class Identity:
    """models an identity from the api"""

    def __init__(self, dict = {}):
        self.id = helpers.get_value(dict, 'id', 0)
        self.id_front_photo = helpers.get_value(dict, 'id_front_photo', '')
        self.id_back_photo = helpers.get_value(dict, 'id_back_photo', '')
        self.owner_photo = helpers.get_value(dict, 'owner_photo', '')
        self.voter_reg_photo = helpers.get_value(dict, 'voter_reg_photo', '')
        self.owner = helpers.get_value(dict, 'owner', '')
        self.properties = Identity.get_properties_from_array(
            helpers.get_value(dict, 'properties', []))

        self.id_number = self.get_property('ID Number')
        self.first_name = self.get_property('First Name')
        self.middle_name = self.get_property('Middle Name')
        self.last_name = self.get_property('Last Name')
        self.date_of_birth = self.get_property('Date of Birth')
        
        self.address_1 = self.get_property('Address Line 1')
        self.address_2 = self.get_property('Address Line 2')
        self.city = self.get_property('City')
        self.state = self.get_property('State')
        self.zip = self.get_property('9-Digit ZIP')
        
        
        

    def __repr__(self):
        return self.to_json()
        
    @staticmethod
    def get_properties_from_array(properties):
        """sets the properties array from an array of property dictionaries"""
        return_properties = []
        for property in properties:
            return_properties.append(IdentityProperty(property))

        return return_properties
    
   

    def get_property(self, name):
        return helpers.get_first(filter(lambda x: x.name == name, self.properties))

   
    def to_dict(self):
        dict1 = {}
        dict = self.__dict__.copy()
        helpers.remove_if_exists(dict, 'properties')
        helpers.remove_if_exists(dict, 'last_name')
        helpers.remove_if_exists(dict, 'first_name')
        helpers.remove_if_exists(dict, 'ssn')
        
        dict['properties'] = map(lambda x: x.__dict__, self.properties)

        return dict

    def to_json(self):
        """convert Identity to json string"""        
        return json.dumps(self.to_dict())



