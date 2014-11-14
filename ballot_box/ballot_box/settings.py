import logging
import os

# Configuration
API_URL = 'http://nathanhourt.com:3001/rpc'
API_USER = 'bob'
API_PASS = 'bob'
DEBUG=True
SECRET_KEY='development_key'
SITE_NAME = 'Follow My Vote - ID Verification'
COMPANY_NAME = 'Follow My Vote'
LOG_LEVEL_FILE = logging.ERROR
LOG_LEVEL_CONSOLE = logging.ERROR
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_LOGS = os.path.join(APP_ROOT, 'logs')
APP_CACHE = os.path.join(APP_ROOT, 'cache')
APP_STATIC = os.path.join(APP_ROOT, 'static')

WALLET_PASSWORD = 'helloworld'
WALLET_NAME = 'default'