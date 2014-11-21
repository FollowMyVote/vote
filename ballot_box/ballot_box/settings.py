import logging
import os
from ballot_box.data.models import Filter

# Configuration
API_URL = 'http://nathanhourt.com:3001/rpc'
API_USER = 'bob'
API_PASS = 'bob'
DEBUG = True
SECRET_KEY = 'development_key'
SITE_NAME = 'Follow My Vote - Ballot Box'
COMPANY_NAME = 'Follow My Vote'
LOG_LEVEL_FILE = logging.ERROR
LOG_LEVEL_CONSOLE = logging.ERROR
APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top
APP_LOGS = os.path.join(APP_ROOT, 'logs')
APP_CACHE = os.path.join(APP_ROOT, 'cache')
APP_STATIC = os.path.join(APP_ROOT, 'static')

WALLET_PASSWORD = 'helloworld'
WALLET_NAME = 'default'

# So at some point we probably need a database to get these values from 
# we can list al tag values, but I don't think that is enough for this demo
BALLOT_BOX_FILTERS = [
    Filter('region', 'Election',
           [('2014 - Mid-term Election - CA', 'STATE')]),
    Filter('district', 'District',
           [('', ''), ('8th', '8th'), ('9th', '9th')]),
    Filter('county', 'County',
           [('', ''), ('Inyo', 'Inyo'), ('Imperial', 'Imperial'), ('Kern', 'Kern')]),
    Filter('precinct', 'Precinct ',
           [('', ''), ('101', '101'), ('102', '102'), ('103', '103')])]


