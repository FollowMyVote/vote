"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

app.config.from_pyfile('settings.py')
import verifier.views
