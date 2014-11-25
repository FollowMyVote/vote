import json
from verifier.modules import helpers
from sqlalchemy import Column, Integer, Table, Text
from sqlalchemy.ext.declarative import declarative_base as real_declarative_base


declarative_base = lambda cls: real_declarative_base(cls=cls)

@declarative_base
class Base(object):
    """
    Add some default properties and methods to the SQLAlchemy declarative base.
    """

    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]

    @property
    def column_items(self):
        return dict([ (c, getattr(self, c)) for c in self.columns])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.column_items)

    def to_json(self):
        return json.dumps(self.column_items)


class Ballot(Base):
    __tablename__ = 'ballot'
    ballot_id = Column(Text, primary_key=True)
    ballot_name = Column(Text, nullable=False)


class Voter(Base):
    __tablename__ = 'voter'

    voter_id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    middle_name = Column(Text)
    last_name = Column(Text)
    suffix = Column(Text)
    address_1 = Column(Text)
    address_2 = Column(Text)
    city = Column(Text)
    state = Column(Text)
    zip = Column(Text)
    birth_date = Column(Text)
    ballot_id = Column(Text)
    precinct = Column(Text)


class VerificationResponse:
    """Models a Verification Response to be sent back to the api"""

    def __init__(self, accepted, rejection_reason, identity, expiration_date,
                 owner_photo_valid, voter_reg_photo_valid,
                 id_front_photo_valid, id_back_photo_valid):
        """initialize a verification response"""
        self.accepted = accepted

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
        """convert object to dict"""
        d = {'accepted': self.accepted}
        if not self.accepted and bool(self.rejection_reason):
            d['rejection_reason'] = self.rejection_reason
        d['verified_identity'] = self.identity.to_dict()
        d['expiration_date'] = self.expiration_date
        d['id_back_photo_valid'] = self.id_back_photo_valid
        d['id_front_photo_valid'] = self.id_front_photo_valid
        d['voter_reg_photo_valid'] = self.voter_reg_photo_valid
        d['owner_photo_valid'] = self.owner_photo_valid

        return d

    def to_json(self):
        """convert object to json string"""
        return json.dumps(self.to_dict())


class IdentityProperty:
    """property value for identity properties"""

    def __init__(self, d=None):
        """initialize an identity property"""
        if not d:
            d = {}
        self.salt = d.get('salt', '')
        self.name = d.get('name', '')
        self.value = d.get('value')
        self.verifier_signatures = d.get('verifier_signatures', [])

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
    FIELD_SUFFIX = 'Name Suffix'
    FIELD_DATE_OF_BIRTH = 'Date of Birth'
    FIELD_ADDRESS_1 = 'Address Line 1'
    FIELD_ADDRESS_2 = 'Address Line 2'
    FIELD_CITY = 'City'
    FIELD_ZIP = 'ZIP'
    FIELD_STATE = 'State'
    FIELD_ID_NUMBER = 'ID Number'
    FIELD_ID_EXPIRATION_DATE = "ID Expiration Date"
    FIELD_REJECTION_REASON = "Rejection Reason"
    FIELD_LABEL_INVALID_IMAGE = "Image Invalid"
    FIELD_BALLOT_ID = "Ballot ID"

    def __init__(self, d=None):
        if not d:
            d = {}
        self.id = d.get('id', 0)
        self.id_front_photo = d.get('id_front_photo', '')
        self.id_back_photo = d.get('id_back_photo', '')
        self.owner_photo = d.get('owner_photo', '')
        self.voter_reg_photo = d.get('voter_reg_photo', '')
        self.owner = d.get('owner', '')
        self.properties = Identity.get_properties_from_array(
            d.get('properties', []))

        self.id_number = self.get_property(Identity.FIELD_ID_NUMBER)
        self.first_name = self.get_property(Identity.FIELD_FIRST_NAME)
        self.middle_name = self.get_property(Identity.FIELD_MIDDLE_NAME)
        self.last_name = self.get_property(Identity.FIELD_LAST_NAME)
        self.suffix = self.get_property(Identity.FIELD_SUFFIX)
        self.date_of_birth = self.get_property(Identity.FIELD_DATE_OF_BIRTH)
        self.ballot_id = self.get_property(Identity.FIELD_BALLOT_ID)

        self.address_1 = self.get_property(Identity.FIELD_ADDRESS_1)
        self.address_2 = self.get_property(Identity.FIELD_ADDRESS_2)
        self.city = self.get_property(Identity.FIELD_CITY)
        self.state = self.get_property(Identity.FIELD_STATE)
        self.zip = self.get_property(Identity.FIELD_ZIP)
        self.ballot_id = self.get_property(Identity.FIELD_BALLOT_ID)

    def __repr__(self):
        return self.to_json()

    @staticmethod
    def get_properties_from_array(properties):
        """sets the properties array from an array of property dictionaries"""
        return_properties = []
        for p in properties:
            return_properties.append(IdentityProperty(p))

        return return_properties

    @staticmethod
    def get_key(request_id):
        """returns a key that can be used to identity this identity"""
        return "verify_request_{0}".format(request_id)

    def get_property(self, name):
        return helpers.get_first(self.properties, lambda x: x.name == name)

    def to_dict(self, include_photos=False):

        if include_photos:
            return dict(owner=self.owner, properties=[x.__dict__.copy() for x in self.properties if bool(x.value)],
                        owner_photo=self.owner_photo, id_front_photo=self.id_front_photo,
                        id_back_photo=self.id_back_photo, voter_reg_photo=self.voter_reg_photo, id=self.id)
        else:
            return dict(owner=self.owner, properties=[x.__dict__.copy() for x in self.properties if bool(x.value)],
                        id=self.id)

    def to_json(self):
        """convert Identity to json string"""
        return json.dumps(self.to_dict())


