from ballot_box import app
from datetime import datetime
from ballot_box.modules import helpers
from flask import Markup
from ballot_box.models import Opinion


@app.context_processor
def processor():
    """set some global data that is available to templates"""
    return dict(datetime=datetime,
                iif=helpers.iif,
                Markup=Markup,
                filter_opinion_summary=Opinion.filter_opinion_summary
    )


