from wtforms import Form, StringField, validators, HiddenField, Field

class VerifyForm(Form):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    ssn = StringField('ID Number')
    id = HiddenField('id')
    result = Field('result')
    
    