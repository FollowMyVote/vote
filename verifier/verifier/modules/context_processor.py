from verifier import app
from datetime import datetime

@app.context_processor
def processor():
    """set some global data that is available to templates"""
    return dict(datetime = datetime)

