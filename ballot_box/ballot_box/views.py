"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for

from ballot_box import app
from ballot_box.modules.helpers import log, alert, date_str_to_iso


@app.route('/')
@app.route('/home')
def home():
    """Get Home Page"""
    log().debug("Render Page: Home")
    return redirect('/ballot-box')
    return render_template('index.html',
        title='Home Page',)



@app.route('/ballot-box')
def ballot_box():
    """Get Balot Box Page"""
    log().debug("Render Page: ballot-box")
    return render_template('ballot-box.html',
        title='Ballot Box',)