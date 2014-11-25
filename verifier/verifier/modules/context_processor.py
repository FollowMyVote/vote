from verifier import app
from datetime import datetime
from verifier.modules import helpers


@app.context_processor
def processor():
    """set some global data that is available to templates"""
    return dict(datetime=datetime)

