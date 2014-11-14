"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for, session
from pprint import pprint

from verifier import app, cache
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

@app.route('/generate')
def generate():
    """Generate Some Test Requests"""
    log().debug("Generate Some Test Requests")
    api.debug_create_test_request(5)
    return redirect('/verify')
    


def update_verify_request_from_form(form, verify_request):
    verify_request.address_1.value = form.address_1.data
    if (bool(form.address_2.data)):
        verify_request.address_2.value = form.address_2.data

    verify_request.first_name.value = form.first_name.data
    verify_request.middle_name.value = form.middle_name.data
    verify_request.last_name.value = form.last_name.data
    verify_request.id_number.value = form.id_number.data

    try:
        if form.date_of_birth.data:
            verify_request.date_of_birth.value = date_str_to_iso(form.date_of_birth.data)
    except:
        pass

    verify_request.city.value = form.city.data
    verify_request.state.value = form.state.data
    verify_request.zip.value = form.zip.data
    return verify_request



@app.route('/verify',  methods=['GET', 'POST'])
def verify():
    """Get Verify Page
    
    TODO: for page rendering performance we should 
    save the base 64 images to a temp file
        
    """
    log().debug("Render Page: Verify")
    verify_request = Identity()
    
    form = VerifyForm(request.form)
    message = ""

    if request.method == 'GET':
        
        verify_request = Identity(api.take_next_request()['result'])
        
        #this line is for testing over and over with the same record you just have to put in the id you want 
        #verify_request = Identity(api.verifier_peek_request(1415817839523482L)['result'])
       
        cache.set(Identity.get_key(verify_request.id), verify_request, 15 * 60)
       
        form.id.data = verify_request.id
        
    elif request.method == 'POST':

        verify_request =  cache.get(Identity.get_key(form.id.data))

                
        pprint(verify_request.first_name)

        if not verify_request:
            verify_request = Identity(api.verifier_peek_request(long(form.id.data))['result'])
        
        
        verify_request = update_verify_request_from_form(form, verify_request)
        print('first name')
        print (verify_request.first_name)
        if form.result.data == 'accept':
            if form.validate():
                if (form.id_back_photo_invalid.data or 
                    form.id_front_photo_invalid.data or 
                    form.owner_photo_invalid.data or 
                    form.voter_reg_photo_invalid.data):
                    message = alert("One or more of the photos have been "
                                    "marked invalid. Invalid photos are not "
                                    "allowed when accepting an id.", "danger")
                else:
                    

                    response = VerificationResponse(True, 
                        None, 
                        verify_request, 
                        date_str_to_iso(form.id_expiration_date.data), 
                        True, 
                        True,
                        True, 
                        True).to_dict()
                

                

                    api.verifier_resolve_request(verify_request.id, response)

                    return redirect('/verify')            
                                                                   
        else:
          #we are rejecting the data make sure we have a reason or an invalid
          #photo
            if (form.rejection_reason.data  or 
                form.id_back_photo_invalid.data or 
                form.id_front_photo_invalid.data or 
                form.owner_photo_invalid.data or 
                form.voter_reg_photo_invalid.data):
                
                response = VerificationResponse(False, 
                    form.rejection_reason.data, 
                    verify_request, 
                    None,
                    not form.owner_photo_invalid.data,
                    not form.voter_reg_photo_invalid.data,
                    not form.id_front_photo_invalid.data, 
                    not form.id_back_photo_invalid.data).to_dict()
              
                api.verifier_resolve_request(verify_request.id,response)

                return redirect('/verify')
            else:
                message = alert("Please enter a rejection reason or select "
                                "an invalid photo", "danger")
                
                


        

    

    return render_template('verify.html',
        title = 'Verify Identity',
        verify_request = verify_request,
        form = form, 
        message = message)


