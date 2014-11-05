import json
from verifier.modules.helpers import get_value

class IdentityProperty:
    """property value for identity properties"""
    
    def __init__(self, dict = {}):
        """initialize an identity property"""
        self.salt = get_value(dict, "salt", "")
        self.name = get_value(dict, "name", "")
        self.value = get_value(dict, "value", None)
        self.verifier_signatures = get_value(dict, "verifier_signatures", [])
        

    def __repr__(self):
        return self.to_json()
       
    def to_json(self):
        """convert IdentityProperty to json string"""
        return json.dumps(self.__dict__)


class Identity:
    """models an identity from the api"""

    def __init__(self, dict = {}):
        
        self.id = get_value(dict, "id", 0)
        self.id_front_photo = get_value(dict, "id_front_photo", "")
        self.id_back_photo = get_value(dict, "id_back_photo", "")
        self.owner_photo = get_value(dict, "owner_photo", "")
        self.voter_reg_photo = get_value(dict, "voter_reg_photo", "")
        self.owner = get_value(dict, "owner", "")
        self.properties = Identity.get_properties_from_array(
            get_value(dict, "properties", []))
        
    @staticmethod
    def get_properties_from_array(properties):
        """sets the properties array from an array of property dictionaries"""
        return_properties = []
        for property in properties:
            return_properties.append(IdentityProperty(property))

        return return_properties


    def get_property(self, name):
        return filter(lambda x: x.name == name, self.properties)


    def __repr__(self):
        return self.to_json()

   

    def to_json(self):
        """convert Identity to json string"""
        return json.dumps(self.__dict__)


