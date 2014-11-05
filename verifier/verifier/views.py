"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request

from verifier import app
from verifier.modules.helpers import log
from verifier.modules import api
from verifier.forms import VerifyForm
from verifier.models import Identity

@app.route("/")
@app.route("/home")
def home():
    """Get Home Page"""
    log().debug("Render Page: Home")
    return render_template("index.html",
        title="Home Page",)


@app.route("/verify",  methods=['GET', 'POST'])

def verify():
    """Get Verify Page"""
    log().debug("Render Page: Verify")
    verify_request = Identity()
    form = VerifyForm(request.form)
    
    if (request.method == 'GET'):
        verify_request = Identity(api.take_next_request()['result'])
    else:
        verify_request = Identity(
            api.verifier_peek_request(long(form.id.data)['result']))

        

    return render_template("verify.html",
        title = "Verify",
        verify_request = verify_request,
        form = form)


