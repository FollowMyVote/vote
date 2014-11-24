"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect

from verifier import app, cache, db
from modules.helpers import log, alert, date_str_to_iso, get_cache
from modules import api
from forms.verify_form import VerifyForm
from data.models import Identity, VerificationResponse



@app.route('/')
@app.route('/home')
def home():
    """Get Home Page"""
    log().debug("Render Page: Home")
    return redirect('/verify')
    return render_template('index.html',
                           title='Home Page', )


@app.route('/generate')
def generate():
    """Generate Some Test Requests"""
    log().debug("Generate Some Test Requests")
    db.generate_test_requests()
    return redirect('/verify')




@app.route('/verify', methods=['GET', 'POST'])
def verify():
    """Get Verify Page
    
    TODO: for page rendering performance we should 
    save the base 64 images to a temp file
        
    """
    log().debug("Render Page: Verify")

    form = VerifyForm(request.form)
    message = ""

    if request.method == 'GET':
        verify_request = form.get()

    elif request.method == 'POST':
        verify_request, message = form.post()
        if not message:
            return redirect('/verify')

    return render_template('verify.html',
                               itle='Verify Identity',
                               verify_request=verify_request,
                               form=form,
                               message=message)

