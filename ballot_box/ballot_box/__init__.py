"""
The flask application package.
"""

from flask import Flask
from ballot_box import settings
from modules.helpers import setup_logging

log = setup_logging(settings.APP_LOGS,
              "ballot_box.log",
              settings.LOG_LEVEL_FILE,
              settings.LOG_LEVEL_CONSOLE)

from ballot_box.data.demo_repository import DemoRepository

from werkzeug.contrib.cache import FileSystemCache

app = Flask(__name__)
app.config.from_pyfile("settings.py")

# you should be able to use any cache that derives from werkzeug.contrib.cache.BaseCache
cache = FileSystemCache(settings.APP_CACHE)

# you should be able to use any repository that derives from  ballot_box.data.base_repository.BaseRepository
db = DemoRepository(settings.DB_CONNECTION_STRING)




import modules.context_processor
import views
from modules import helpers


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.end_session()
