from wtforms import Form, FileField, StringField, SubmitField, validators, IntegerField, ValidationError, form, EmailField, SelectField, PasswordField, TextAreaField
# import wtforms
from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize, FileStorage
from flask_uploads import UploadSet, IMAGES, configure_uploads


class SignUpForm(Form):
    # def __init__(self, photo, *args, **kwargs):
    #     self.photos = photo
    #     # got the correction from the link below
    #     # https://stackoverflow.com/questions/61953652/modifying-flaskforms-class-object-has-no-attribute-fields
    #     super(SignUpForm, self).__init__(*args, **kwargs)

    name = StringField('Name', validators=[validators.input_required(), validators.length(min=1, max=100)],
                       render_kw={"placeholder": "Enter the name you want on the quotation "})
    email = EmailField('Email', validators=[validators.input_required()],
                       render_kw={"placeholder": "Enter the email you want on the quotation "})

    password = PasswordField('Password', validators=[validators.input_required()],
                            render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign up')