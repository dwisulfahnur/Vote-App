from flask_wtf import Form
from wtforms import StringField, DateField, validators

class InputID(Form):
    full_name = StringField('Your name', [validators.Required('Enter your Full Name')])
    email = StringField('Your mail', [validators.Required('Enter your Mail')])
    birthday = DateField('Your Birth Date', format="%Y-%m-%d")
