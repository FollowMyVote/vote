from wtforms import Form, validators, HiddenField, StringField, SelectField, BooleanField
from verifier.models import Identity
from verifier import settings


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

    id_number = StringField(
        Identity.FIELD_ID_NUMBER,
        [validators.DataRequired(),
         validators.Length(max=50)])

    id_expiration_date = StringField(
        Identity.FIELD_ID_EXPIRATION_DATE,
        [validators.DataRequired(),
         validators.Regexp(r'\d{1,2}/\d{1,2}/\d{4}',
                           message="This field is not a valid date. "
                                   "Format: MM/DD/YYYY")])

    date_of_birth = StringField(
        Identity.FIELD_DATE_OF_BIRTH,
        [validators.DataRequired(),
         validators.Regexp(r'\d{1,2}/\d{1,2}/\d{4}',
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

    state = SelectField(
        Identity.FIELD_STATE,
        [validators.DataRequired()],
        choices=settings.STATES)

    ballot_id = SelectField(
        Identity.ballot_id,
        [validators.DataRequired()],
        choices=settings.STATES)

    zip = StringField(
        Identity.FIELD_ZIP,
        [validators.DataRequired(),
         validators.Regexp(r'\d{5}-\d{4}',
                           message="This field must be a 9 digit zip code. "
                                   "Format: 99999-9999")])

    rejection_reason = SelectField(
        Identity.FIELD_REJECTION_REASON,
        choices=settings.REJECTION_REASONS)

    owner_photo_invalid = BooleanField(Identity.FIELD_LABEL_INVALID_IMAGE)
    voter_reg_photo_invalid = BooleanField(Identity.FIELD_LABEL_INVALID_IMAGE)
    id_front_photo_invalid = BooleanField(Identity.FIELD_LABEL_INVALID_IMAGE)
    id_back_photo_invalid = BooleanField(Identity.FIELD_LABEL_INVALID_IMAGE)

    id = HiddenField('id')
    result = HiddenField('result')
