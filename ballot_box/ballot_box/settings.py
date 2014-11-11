import logging
import os

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
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_LOGS = os.path.join(APP_ROOT, 'logs')