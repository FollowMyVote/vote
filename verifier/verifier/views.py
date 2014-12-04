"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect, url_for, jsonify
from verifier import app, cache, db, log
from modules.helpers import  alert, date_str_to_iso, get_cache
from forms.verify_form import VerifyForm
from data.models import Identity, VerificationResponse



@app.route('/')
def home():
    """Get Home Page"""
    log.debug("Render Page: Home")
    return render_template('index.html',
                           title='Home Page', )


@app.route('/generate')
def generate():
    """Generate Some Test Requests"""
    log.debug("Generate Some Test Requests")
    db.generate_test_requests()
    return redirect(url_for('verify'))



@app.route('/search-voters')
def search_voters():
    """search for voters and return the results"""

    query = request.args.get('query')
    search_terms = query.split()
    results = db.search_voters(search_terms)
    if results:
        return jsonify(results=[r.column_items for r in results])
    else:
        return jsonify(results=[])



@app.route('/verify', methods=['GET', 'POST'])
def verify():
    """Get Verify Page
    
    TODO: for page rendering performance we should 
    save the base 64 images to a temp file
        
    """
    log.debug("Render Page: Verify")
    log.debug("Render Page: Verify")

    form = VerifyForm(request.form)
    message = ""

    if request.method == 'GET':
        verify_request = form.get(request)

    elif request.method == 'POST':
        verify_request, message = form.post()
        if not message:
            return redirect(url_for('verify'))

    return render_template('verify.html',
                               title='Verify Identity',
                               verify_request=verify_request,
                               form=form,
                               message=message)


@app.route('/pending')
def pending():
    """show pending requests"""
    return render_template('list_requests.html',
                           title='Pending Requests',
                           requests=db.get_identities(Identity.STATUS_AWAITING_PROCESSING)

    )

@app.route('/in-process')
def in_process():
    """show in process request"""
    return render_template('list_requests.html',
                           title='In Process Requests',
                           requests=db.get_identities(Identity.STATUS_IN_PROCESSING)

    )