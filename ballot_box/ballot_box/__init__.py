"""
The flask application package.
"""

from flask import Flask
from ballot_box import settings
from werkzeug.contrib.cache import FileSystemCache

app = Flask(__name__)
app.config.from_pyfile("settings.py")

cache = FileSystemCache(settings.APP_CACHE)

from modules.helpers import setup_logging
setup_logging(settings.APP_LOGS, 
              "ballot_box.log", 
              settings.LOG_LEVEL_FILE,
              settings.LOG_LEVEL_CONSOLE)

import modules.context_processor
import views
from modules import helpers
