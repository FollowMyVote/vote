from ballot_box import app
from datetime import datetime
from ballot_box.modules import helpers

@app.context_processor
def processor():
    """set some global data that is available to templates"""
    return dict(datetime = datetime,
                iif = helpers.iif)

