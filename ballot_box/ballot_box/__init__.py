"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.config.from_pyfile("settings.py")

from ballot_box.modules.helpers import setup_logging
setup_logging()

import ballot_box.modules.context_processor
import ballot_box.views
from ballot_box.modules import helpers
