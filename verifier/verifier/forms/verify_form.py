from wtforms import Form, validators, HiddenField, StringField, SelectField, BooleanField
from verifier.data.models import Identity, VerificationResponse
from verifier.modules.helpers import  date_str_to_iso, get_cache, alert
from verifier import settings, db, cache


class VerifyForm(Form):
    first_name = StringField(
        Identity.FIELD_FIRST_NAME,
        [validators.DataRequired(),
         validators.Length(max=50)])

    middle_name = StringField(
        Identity.FIELD_MIDDLE_NAME,
        [validators.Length(max=50)])

    last_name = StringField(
        Identity.FIELD_LAST_NAME,
        [validators.DataRequired(),
         validators.Length(max=50)])

    suffix = StringField(
        'Suffix',
        [validators.Length(max=50)])


    id_number = StringField(
        Identity.FIELD_ID_NUMBER,
        [validators.DataRequired(),
         validators.Length(max=50)])

    id_expiration_date = StringField(
        Identity.FIELD_ID_EXPIRATION_DATE,
        [validators.DataRequired(),
         validators.Regexp(r'^(?:[1-9]|1[012])/([1-9]|[12][0-9]|3[01])/(19|20)\d\d$',
                           message="This field is not a valid date. "
                                   "Format: MM/DD/YYYY")])

    birth_date = StringField(
        Identity.FIELD_DATE_OF_BIRTH,
        [validators.DataRequired(),
         validators.Regexp(r'^(?:[1-9]|1[012])/([1-9]|[12][0-9]|3[01])/(19|20)\d\d$',
                           message="This field is not a valid date. "
                                   "Format: MM/DD/YYYY")])

    address_1 = StringField(
        Identity.FIELD_ADDRESS_1,
        [validators.DataRequired(),
         validators.Length(max=150)])

    address_2 = StringField(
        Identity.FIELD_ADDRESS_2,
        [validators.Length(max=150)])

    city = StringField(
        Identity.FIELD_CITY,
        [validators.DataRequired(),
         validators.Length(max=50)])

    state = HiddenField()

    ballot_id = HiddenField()

    zip = StringField(
        Identity.FIELD_ZIP,
        [validators.DataRequired(),
         validators.Regexp(r'^(?:\d{5}-\d{4}|\d{5})',
                           message="This field must be a 5 or 9 digit zip code. "
                                   "Format: 99999 or 99999-9999")])

    rejection_reason = SelectField(
        Identity.FIELD_REJECTION_REASON,
        choices=settings.REJECTION_REASONS)

    owner_photo_invalid = BooleanField(Identity.FIELD_LABEL_INVALID_IMAGE)
    voter_reg_photo_invalid = BooleanField(Identity.FIELD_LABEL_INVALID_IMAGE)
    id_front_photo_invalid = BooleanField(Identity.FIELD_LABEL_INVALID_IMAGE)
    id_back_photo_invalid = BooleanField(Identity.FIELD_LABEL_INVALID_IMAGE)

    id = HiddenField()
    result = HiddenField()


    state_select = SelectField(Identity.FIELD_STATE,
                               [validators.optional()],
                               choices=settings.STATES)
    _ballots = [('', 'Select Ballot...')] + [(b.ballot_id, b.ballot_name) for b in db.get_ballots()]
    ballot_id_select = SelectField( 'Ballot',
                                    [validators.optional()],
                                    choices=_ballots)



    def get(self):
        """do get processing"""
        verify_request = db.get_next_identity()
        # this line is for testing over and over with the same record you just have to put in the id you want
        #verify_request = db.get_identity(1417020710343152L)



        cache.set(Identity.get_key(verify_request.id), verify_request, 15 * 60)
        self.id.data = verify_request.id
        return verify_request

    def update_verify_request(self, verify_request):
        """updates a verification request using form data"""
        verify_request.address_1.value = self.address_1.data
        if bool(self.address_2.data):
            verify_request.address_2.value = self.address_2.data

        verify_request.first_name.value = self.first_name.data
        verify_request.middle_name.value = self.middle_name.data
        verify_request.suffix.value = self.suffix.data
        verify_request.last_name.value = self.last_name.data
        verify_request.id_number.value = self.id_number.data

        try:
            if self.date_of_birth.data:
                verify_request.date_of_birth.value = date_str_to_iso(self.date_of_birth.data)
        except:
            pass

        verify_request.city.value = self.city.data
        verify_request.state.value = self.state.data
        verify_request.ballot_id.value = self.ballot_id.data
        verify_request.zip.value = self.zip.data
        return verify_request

    def get_request(self):
        """get the current request being verified"""
        def get_request():
            return db.get_identity(long(self.id.data))

        verify_request = get_cache(cache, Identity.get_key(self.id.data), get_request, 15 * 60)

        if not verify_request:
            verify_request = db.get_identity(self.id.data)

        return self.update_verify_request(verify_request)

    def post(self):
        """process a post request  do a verification or return validation errors"""

        verify_request =  self.get_request()
        message = ""
        if self.result.data == 'accept':

            if self.validate():
                if (self.id_back_photo_invalid.data or
                        self.id_front_photo_invalid.data or
                        self.owner_photo_invalid.data or
                        self.voter_reg_photo_invalid.data):
                    message = alert("One or more of the photos have been "
                                    "marked invalid. Invalid photos are not "
                                    "allowed when accepting an id.", "danger")
                elif not self.state.data:
                    message = alert("State selection is invalid", "danger")
                elif not self.ballot_id.data:
                    message = alert("Ballot ID is invalid", "danger")
                else:
                    response = VerificationResponse(True,
                                                    None,
                                                    verify_request,
                                                    date_str_to_iso(self.id_expiration_date.data),
                                                    True,
                                                    True,
                                                    True,
                                                    True)

                    db.resolve_request(verify_request.id, response)



        else:
            # we are rejecting the data make sure we have a reason or an invalid
            # photo
            if (self.rejection_reason.data or
                    self.id_back_photo_invalid.data or
                    self.id_front_photo_invalid.data or
                    self.owner_photo_invalid.data or
                    self.voter_reg_photo_invalid.data):

                response = VerificationResponse(False,
                                                self.rejection_reason.data,
                                                verify_request,
                                                None,
                                                not self.owner_photo_invalid.data,
                                                not self.voter_reg_photo_invalid.data,
                                                not self.id_front_photo_invalid.data,
                                                not self.id_back_photo_invalid.data)

                db.resolve_request(verify_request.id, response)

            else:
                message = alert("Please enter a rejection reason or select "
                                "an invalid photo", "danger")

        return verify_request, message