"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for
from pprint import pprint
from ballot_box import app, settings, cache
from ballot_box.forms import BallotBoxForm
from ballot_box.modules import api
from ballot_box.models import Contest
from ballot_box.modules.helpers import log, alert, date_str_to_iso, get_cache



@app.route('/')
@app.route('/home')
def home():
    """Get Home Page"""
    log().debug("Render Page: Home")
    return redirect('/ballot-box')
    return render_template('index.html',
        title='Home Page',)


def get_all_contests():

    def get_all_contests_internal():
        contest_ids = api.ballot_get_all_contests()['result']
        return [ Contest(c, api.ballot_get_contest_by_id(c)['result']) for c in contest_ids]

    return get_cache(cache, 'all_contests', get_all_contests_internal)


def get_filtered_contests(form):
    """ Filters contests by the form filters """
    contests = get_all_contests()
    
    
    
    for f in form.filters:
        if f.value:
            contests = [c for c in contests if c.tag(f.name) == f.value]

        if not contests:
            break

    if contests and form.search:
        contests = [c for c in contests if c.search(form.search)]


    
    return contests
            
    


@app.route('/ballot-box', methods=['GET', 'POST'])
def ballot_box():
    """Get Balot Box Page"""
    log().debug("Render Page: ballot-box")
    form = BallotBoxForm(request, settings.BALLOT_BOX_FILTERS)
    form.contests = get_filtered_contests(form)
    
    return render_template('ballot-box.html',
        title = 'Ballot Box',
        form = form)