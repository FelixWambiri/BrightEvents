from wtforms import StringField, Form, validators, PasswordField

"""
This class will help validate the registration form
"""


class RegisterForm(Form):
    username = StringField('Username',
                           [validators.DataRequired("Please fill out this field"), validators.Length(min=5, max=30)])

    email = StringField('Email', [validators.Email("Not a valid email address"),
                                  validators.DataRequired("Please fill out this field")])

    password = PasswordField('Password', [validators.DataRequired("Please fill out this field"),
                                          validators.EqualTo('confirm_password', message='Passwords do not match')])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired("This field is a Must")])

