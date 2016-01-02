from flask_wtf import Form
from wtforms import StringField, DateField, validators

class InputID(Form):
    full_name = StringField('Your name', [validators.Required()])
    email = StringField('Your mail', [validators.Required()])
    birthday = DateField('Your Birth Date', format="%Y-%m-%d")
