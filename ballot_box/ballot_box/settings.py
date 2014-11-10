import logging
# Configuration
API_URL = 'http://192.168.1.7:3001/rpc'
API_USER = 'bob'
API_PASS = 'bob'
DEBUG=True
SECRET_KEY='development_key'
SITE_NAME = 'Follow My Vote - Ballot Box'
COMPANY_NAME = 'Follow My Vote'
LOG_LEVEL_FILE = logging.ERROR
LOG_LEVEL_CONSOLE = logging.DEBUG

STATES = [
          ('', 'None'),
          ('AL', 'Alabama'), 
          ('AK', 'Alaska'), 
          ('AS', 'American Samoa'), 
          ('AZ', 'Arizona'), 
          ('AR', 'Arkansas'),
          ('AE', 'Armed Forces Africa'), 
          ('AA', 'Armed Forces Americas'), 
          ('AE', 'Armed Forces Canada'), 
          ('AE', 'Armed Forces Europe'), 
          ('AE', 'Armed Forces Middle East'), 
          ('AP', 'Armed Forces Pacific'),  
          ('CA', 'California'), 
          ('CO', 'Colorado'), 
          ('CT', 'Connecticut'), 
          ('DE', 'Delaware'), 
          ('DC', 'District Of Columbia'), 
          ('FM', 'Federated States Of Micronesia'), 
          ('FL', 'Florida'), 
          ('GA', 'Georgia'), 
          ('GU', 'Guam'), 
          ('HI', 'Hawaii'), 
          ('ID', 'Idaho'), 
          ('IL', 'Illinois'), 
          ('IN', 'Indiana'), 
          ('IA', 'Iowa'), 
          ('KS', 'Kansas'), 
          ('KY', 'Kentucky'), 
          ('LA', 'Louisiana'), 
          ('ME', 'Maine'), 
          ('MH', 'Marshall Islands'), 
          ('MD', 'Maryland'), 
          ('MA', 'Massachusetts'), 
          ('MI', 'Michigan'), 
          ('MN', 'Minnesota'), 
          ('MS', 'Mississippi'), 
          ('MO', 'Missouri'), 
          ('MT', 'Montana'), 
          ('NE', 'Nebraska'), 
          ('NV', 'Nevada'), 
          ('NH', 'New Hampshire'), 
          ('NJ', 'New Jersey'), 
          ('NM', 'New Mexico'), 
          ('NY', 'New York'), 
          ('NC', 'North Carolina'), 
          ('ND', 'North Dakota'), 
          ('MP', 'Northern Mariana Islands'), 
          ('OH', 'Ohio'), 
          ('OK', 'Oklahoma'), 
          ('OR', 'Oregon'), 
          ('PW', 'Palau'), 
          ('PA', 'Pennsylvania'), 
          ('PR', 'Puerto Rico'), 
          ('RI', 'Rhode Island'), 
          ('SC', 'South Carolina'), 
          ('SD', 'South Dakota'), 
          ('TN', 'Tennessee'), 
          ('TX', 'Texas'), 
          ('UT', 'Utah'), 
          ('VT', 'Vermont'), 
          ('VI', 'Virgin Islands'), 
          ('VA', 'Virginia'), 
          ('WA', 'Washington'), 
          ('WV', 'West Virginia'), 
          ('WI', 'Wisconsin'), 
          ('WY', 'Wyoming')]


REJECTION_REASONS = [
                     ('', 'None'), 
                     ('ID not legible', 'ID not legible'), 
                     ('Registration not legible', 'Registration not legible'), 
                     ('Photos do not match', 'Photos do not match'), 
                     ('Expired ID', 'Expired ID'), 
                     ('Expired Registration', 'Expired Registration')] 

