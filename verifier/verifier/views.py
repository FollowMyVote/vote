"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from verifier import app
from verifier.modules.helpers import log
import verifier.modules.api

@app.route("/")
@app.route("/home")
def home():
    """Get Home Page"""
    log().debug("Render Page: Home")
    return render_template(
        "index.html",
        title="Home Page",
        
    )


@app.route("/verify")
def verify():
    """Get Verify Page"""
    log().debug("Render Page: Verify")
    return render_template(
        "verify.html",
        title="Verify",
        
    )


