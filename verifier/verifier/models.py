import json
from verifier.modules import helpers

class VerificationResponse:
    def __init__(self, accepted, rejection_reason, identity, expiration_date, 
                 owner_photo_valid, voter_reg_photo_valid, 
                 id_front_photo_valid, id_back_photo_valid):

        """initialize a verification response"""
        self.accepted = accepted
        if rejection_reason:
            self.rejection_reason = rejection_reason

        self.identity = identity
        self.expiration_date = expiration_date
        self.owner_photo_valid = owner_photo_valid
        self.id_back_photo_valid = id_back_photo_valid
        self.id_front_photo_valid = id_front_photo_valid
        self.voter_reg_photo_valid = voter_reg_photo_valid

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """conver object to dict"""
        dict =  {'accepted': self.accepted}
        if not self.accepted:
            dict['rejection_reason'] = self.rejection_reason
        dict['verified_identity'] = self.identity.to_dict()
        dict['expiration_date'] = self.expiration_date
        dict['id_back_photo_valid'] = self.id_back_photo_valid
        dict['id_front_photo_valid'] = self.id_front_photo_valid
        dict['voter_reg_photo_valid'] = self.voter_reg_photo_valid
        dict['owner_photo_valid'] = self.owner_photo_valid

        return dict

    def to_json(self):
        """convert object to json string"""
        return json.dumps(self.to_dict())




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
    FIELD_FIRST_NAME = 'First Name'
    FIELD_LAST_NAME = 'Last Name'
    FIELD_MIDDLE_NAME = 'Middle Name'
    FIELD_DATE_OF_BIRTH = 'Date of Birth'
    FIELD_ADDRESS_1 = 'Address Line 1'
    FIELD_ADDRESS_2 = 'Address Line 2'
    FIELD_CITY = 'City'
    FIELD_ZIP = '9-Digit ZIP'
    FIELD_STATE = 'State'
    FIELD_ID_NUMBER = 'ID Number'
    FIELD_ID_EXPIRATION_DATE = "ID Expiration Date"
    FIELD_REJECTION_REASON = "Rejection Reason"
    FIELD_LABEL_INVALID_IMAGE = "Image Invalid"

    def __init__(self, dict = {}):
        self.id = helpers.get_value(dict, 'id', 0)
        self.id_front_photo = helpers.get_value(dict, 'id_front_photo', '')
        self.id_back_photo = helpers.get_value(dict, 'id_back_photo', '')
        self.owner_photo = helpers.get_value(dict, 'owner_photo', '')
        self.voter_reg_photo = helpers.get_value(dict, 'voter_reg_photo', '')
        self.owner = helpers.get_value(dict, 'owner', '')
        self.properties = Identity.get_properties_from_array(
            helpers.get_value(dict, 'properties', []))
        
        self.id_number = self.get_property(Identity.FIELD_ID_NUMBER)
        self.first_name = self.get_property(Identity.FIELD_FIRST_NAME)
        self.middle_name = self.get_property(Identity.FIELD_MIDDLE_NAME)
        self.last_name = self.get_property(Identity.FIELD_LAST_NAME)
        self.date_of_birth = self.get_property(Identity.FIELD_DATE_OF_BIRTH)
        
        self.address_1 = self.get_property(Identity.FIELD_ADDRESS_1)
        self.address_2 = self.get_property(Identity.FIELD_ADDRESS_2)
        self.city = self.get_property(Identity.FIELD_CITY)
        self.state = self.get_property(Identity.FIELD_STATE)
        self.zip = self.get_property(Identity.FIELD_ZIP)
        
        
        

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
        
        return {'owner': self.owner,
                'properties': map(lambda x: x.__dict__, 
                                  filter(lambda y: bool(y.value), self.properties)),
                'owner_photo': self.owner_photo,
                'id_front_photo': self.id_front_photo,
                'voter_reg_photo': self.voter_reg_photo,
                'id': self.id                
                }
    

    def to_json(self):
        """convert Identity to json string"""        
        return json.dumps(self.to_dict())



