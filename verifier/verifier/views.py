"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from verifier import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/verify')
def verify():
    """Renders the about page."""
    return render_template(
        'verify.html',
        title='Verify',
        year=datetime.now().year,
        message='Your application description page.'
    )


