from verifier import app
from datetime import datetime

@app.context_processor
def processor():
    return dict(datetime = datetime)

