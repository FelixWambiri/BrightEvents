from wtforms import StringField, Form, validators, PasswordField, TextAreaField

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


class CreateEventForm(Form):
    name = StringField('Name',
                       [validators.DataRequired("Please fill out this field"), validators.Length(min=5, max=30)])
    category = StringField('Category',
                           [validators.DataRequired("Please fill out this field"), validators.Length(min=5, max=30)])
    location = StringField('Location',
                           [validators.DataRequired("Please fill out this field"), validators.Length(min=5, max=30)])
    owner = StringField('Owner',
                        [validators.DataRequired("Please fill out this field"), validators.Length(min=5, max=30)])
    description = TextAreaField('Description', [validators.Length(min=15)])


class UpdateEventForm(Form):
    name = StringField('Name')

    category = StringField('Category')

    location = StringField('Location')

    owner = StringField('Owner')

    description = TextAreaField('Description')


class ResetPasswordForm(Form):
    previous_password = PasswordField('Previous Password', [validators.DataRequired("Please fill out this field")])
    new_password = PasswordField('New Password', [validators.DataRequired("Please fill out this field")])
