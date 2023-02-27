
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import email_validator

class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[
        DataRequired(),
        Length(min=1, max=30)
    ])
    last_name = StringField('Last name', validators=[
        DataRequired(),
        Length(min=1, max=30)
    ])
    # TODO: E-Mail can only be @miamioh.edu
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    # NOTE: Maybe implement secure passwords?
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8)
    ])
    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me?')
    submit = SubmitField('Login')

