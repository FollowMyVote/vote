"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for

from verifier import app
from verifier.modules.helpers import log, alert, date_str_to_iso
from verifier.modules import api
from verifier.forms import VerifyForm
from verifier.models import Identity, VerificationResponse

@app.route('/')
@app.route('/home')
def home():
    """Get Home Page"""
    log().debug("Render Page: Home")
    return redirect('/verify')
    return render_template('index.html',
        title='Home Page',)


def update_verify_request_from_from(form, verify_request):
    verify_request.address_1.value = form.address_1.data
    if (bool(form.address_2.data)):
        verify_request.address_2.value = form.address_2.data

    verify_request.first_name = form.first_name.data
    verify_request.middle_name = form.middle_name.data
    verify_request.last_name = form.last_name.data
    verify_request.id_number = form.id_number.data
    verify_request.date_of_birth = date_str_to_iso(form.date_of_birth.data)
    verify_request.city = form.city.data
    verify_request.state = form.state.data
    verify_request.zip = form.zip.data
    return verify_request



@app.route('/verify',  methods=['GET', 'POST'])
def verify():
    """Get Verify Page"""
    log().debug("Render Page: Verify")
    verify_request = Identity()
    
    form = VerifyForm(request.form)
    message = ""

    if request.method == 'GET':
        verify_request = Identity(api.take_next_request()['result'])
        form.id.data = verify_request.id
        #form.first_name = verify_request.
    elif request.method == 'POST':
        verify_request = Identity(
            api.verifier_peek_request(long(form.id.data))['result'])
        
        
        if form.result.data == 'accept':
            if form.validate():
                verify_request = update_verify_request_from_from(
                    form, verify_request)

                response = VerificationResponse(
                    True, 
                    None, 
                    verify_request, 
                    date_str_to_iso(form.id_expiration_date.data)).to_dict()
                
                
                api.verifier_resolve_request(
                    verify_request.id, response)

                return redirect('/verify')
                                                                   
        else:
            if form.rejection_reason.data != '' :

                response =  VerificationResponse(
                    False, 
                    form.rejection_reason.data, 
                    verify_request, 
                    None).to_dict()

                api.verifier_resolve_request(
                    verify_request.id,response)

                return redirect('/verify')
            else:
                message = alert("Please enter a rejection reason", "danger")
                
                


        

    

    return render_template('verify.html',
        title = 'Verify Identity',
        verify_request = verify_request,
        form = form, 
        message = message)


