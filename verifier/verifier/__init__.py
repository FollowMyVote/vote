"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.config.from_pyfile("settings.py")

from verifier.modules.helpers import setup_logging
setup_logging()

import modules.context_processor
import verifier.views
from verifier.modules import helpers
from jinja2 import Environment

env = Environment()
env.globals['iif_test'] = helpers.iif



