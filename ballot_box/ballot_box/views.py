"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect
from ballot_box import app, settings, cache, db, log
from ballot_box.forms import BallotBoxForm
from ballot_box.modules import api
from ballot_box.data.models import Contest, Decision, Opinion
from ballot_box.modules.helpers import get_cache

@app.route('/')
@app.route('/home')
def home():
    """Get Home Page"""
    log.debug("Render Page: Home")
    return redirect('/ballot-box')
    return render_template('index.html',
                           title='Home Page', )


@app.route('/ballot-box', methods=['GET', 'POST'])
def ballot_box():
    """Get Ballot Box Page"""
    log.debug("Render Page: ballot-box")
    form = BallotBoxForm(request, settings.BALLOT_BOX_FILTERS)
    contests = db.get_all_contests()
    form.contests = form.get_filtered_contests(contests)
    form.contest_groups = form.get_contest_groups(form.contests)
    form.set_form_contest()

    return render_template('ballot-box.html',
                           title='Ballot Box',
                           form=form)