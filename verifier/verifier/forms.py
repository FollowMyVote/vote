from wtforms import Form, StringField, validators, HiddenField

class VerifyForm(Form):
    firstname = StringField('First Name')
    lastname = StringField('Email Address')
    ssn = StringField('Email Address')
    id = HiddenField('id')
    