import unittest

from verifier.models import Identity, IdentityProperty, VerificationResponse


class TestIdentityProperty(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        d = {u'salt': u'234',
             u'name': u'LastName',
             u'value': None,
             u'verifier_signatures': []}
        self.empty_property = IdentityProperty()
        self.property = IdentityProperty(d)

    def test_identity_property_empty(self):
        self.assertEquals(self.empty_property.name, "")

    def test_identity_property_last_name(self):
        self.assertEquals(self.property.name, "LastName")

    def test_identity_property_to_json(self):
        self.property.to_json()


class TestVerificationResponse(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""

        self.response = VerificationResponse(
            True, 'rejection reason', Identity(), '2014-1-1', True, True,
            True, False)

    def test_verification_response_property_accepted(self):
        self.assertTrue(self.response.accepted)

    def test_verification_response_to_json(self):
        self.response.to_json()

    def test_verification_response_to_dict(self):
        self.assertEquals(self.response.to_dict()['expiration_date'],
                          '2014-1-1')


class TestIdentity(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        d = {
            "owner": "XTS79bJheDVN8bpACsN5y2p3mUbv6Tv5wCtn",
            "properties": [
                {
                    "salt": "123",
                    "name": "First Name",
                    "value": "FirstName",
                    "verifier_signatures": []
                },
                {
                    "salt": "666",
                    "name": "Middle Name",
                    "value": None,
                    "verifier_signatures": []
                },
                {
                    "salt": "234",
                    "name": "Last Name",
                    "value": None,
                    "verifier_signatures": []
                },
                {
                    "salt": "777",
                    "name": "Date of Birth",
                    "value": None,
                    "verifier_signatures": []
                },
                {
                    "salt": "345",
                    "name": "ID Number",
                    "value": None,
                    "verifier_signatures": []
                },
                {
                    "salt": "3456",
                    "name": "Address Line 1",
                    "value": None,
                    "verifier_signatures": []
                },
                {
                    "salt": "34567",
                    "name": "Address Line 2",
                    "value": None,
                    "verifier_signatures": []
                },
                {
                    "salt": "34567",
                    "name": "City",
                    "value": None,
                    "verifier_signatures": []
                },
                {
                    "salt": "543",
                    "name": "State",
                    "value": None,
                    "verifier_signatures": []
                },
                {
                    "salt": "5432",
                    "name": "9-Digit ZIP",
                    "value": None,
                    "verifier_signatures": []
                }],
            "owner_photo": "owner_photo",
            "id_front_photo": "id front",
            "id_back_photo": "id back",
            "voter_reg_photo": "voter reg",
            "id": 1415313067144342}

        self.empty_identity = Identity()
        self.identity = Identity(d)

    def test_identity_get_properties_from_array(self):
        x = [
            {
                "salt": "123",
                "name": "First Name",
                "value": "FirstName",
                "verifier_signatures": []
            },
            {
                "salt": "666",
                "name": "Middle Name",
                "value": None,
                "verifier_signatures": []
            },
            {
                "salt": "234",
                "name": "Last Name",
                "value": None,
                "verifier_signatures": []
            },
            {
                "salt": "777",
                "name": "Date of Birth",
                "value": None,
                "verifier_signatures": []
            },
            {
                "salt": "345",
                "name": "ID Number",
                "value": None,
                "verifier_signatures": []
            },
            {
                "salt": "3456",
                "name": "Address Line 1",
                "value": None,
                "verifier_signatures": []
            },
            {
                "salt": "34567",
                "name": "Address Line 2",
                "value": None,
                "verifier_signatures": []
            },
            {
                "salt": "34567",
                "name": "City",
                "value": None,
                "verifier_signatures": []
            },
            {
                "salt": "543",
                "name": "State",
                "value": None,
                "verifier_signatures": []
            },
            {
                "salt": "5432",
                "name": "9-Digit ZIP",
                "value": None,
                "verifier_signatures": []
            }]

        properties = Identity.get_properties_from_array(x)

        self.assertEquals(len(properties), 10)
        self.assertEquals(properties[0].name, "First Name")

        x = []
        properties = Identity.get_properties_from_array(x)
        self.assertEquals(len(properties), 0)

    def test_identity_empty(self):
        self.assertEquals(self.empty_identity.id, 0)

    def test_identity_properties(self):
        self.assertIsNotNone(self.identity.properties)
        self.assertEquals(self.identity.properties[0].name, 'First Name')

    def test_identity_property(self):
        self.assertEquals(self.identity.id_back_photo, 'id back')

    def test_identity_to_dict(self):
        d = self.identity.to_dict(True)
        self.assertIsNotNone(d)
        self.assertEquals(d['id_front_photo'], 'id front')
        self.assertEquals(len(d['properties']), 1)

    def test_identity_to_json(self):
        self.identity.to_json()


if __name__ == "__main__":
    unittest.main()