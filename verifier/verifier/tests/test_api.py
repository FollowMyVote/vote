import unittest
import time
from pprint import pprint
from verifier.modules import api
from verifier.models import Identity, IdentityProperty, VerificationResponse
from datetime import date, datetime



def create_request():
    account_name = api.get_unique_account_name()
    api.wallet_account_create(account_name)
    request = api.debug_request_verification(
        account_name,
        "owner_photo",
        "id front",
        "id back",
        "voter reg")
    return request

class TestAPI(unittest.TestCase):
    

    def setUp(self):
        """Call before every test case."""
        api.wallet_open('default')
        api.wallet_unlock(99999999, 'helloworld')
    
    def tearDown(self):
        """call after every test case."""
        api.wallet_open('default')
        api.wallet_unlock(99999999, 'helloworld')

    def test_api_close_wallet(self):
        self.assertEqual(api.wallet_close()['result'], None)
    
    def test_api_get_random_account_name(self):
        self.assertIsNotNone(api.get_unique_account_name())

    def test_api_wallet_account_create(self):
        response = api.wallet_account_create(api.get_unique_account_name())
        self.assertIsNotNone(response['result'])
        
    
    def test_api_debug_request_verification(self):
        response = create_request();
        self.assertFalse("error" in response);
        self.assertIsNotNone(response['result'])

    def test_api_take_next_request(self):
        self.assertIsNotNone(api.take_next_request()['result'])


    def test_api_verifier_peek_request(self):
        create_request()
        id = api.verifier_list_requests()['result'][0]['id']
        response = api.verifier_peek_request(id);
        self.assertFalse("error" in response);
        self.assertIsNotNone(response['result'])

    def test_api_verifier_list_requests(self):
        self.assertIsNotNone(api.verifier_list_requests()['result'])

    def test_api_verifier_resolve_request(self):
        create_request()
        verify_request = Identity(api.take_next_request()['result'])

        today = datetime.combine(date.today(), datetime.min.time())
        x = VerificationResponse(True, None, verify_request, today.isoformat(),
                                 True, True, True, True)
        
        response = api.verifier_resolve_request(verify_request.id, x.to_dict())
        self.assertFalse("error" in response);

        create_request()
        verify_request = Identity(api.take_next_request()['result'])
        x = VerificationResponse(False, "this is the rejection reason", 
                                 verify_request, None, True, True, False, True)
        
        response = api.verifier_resolve_request(verify_request.id, x.to_dict())
        self.assertFalse("error" in response);
        
          

  

if __name__ == "__main__":
    unittest.main()

    
    