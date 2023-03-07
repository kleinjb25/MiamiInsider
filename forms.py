
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator

def validate_email_domain(form, field):
    email = field.data
    domain = email.split('@')[1] # Get the domain from the email
    if domain != 'miamioh.edu': # Check if domain is not miamioh.edu
        raise ValidationError('Email must be of @miamioh.edu domain')

# NOTE: These are all available, only password_contains_number being used right now
def password_contains_special(form, field):
    if not any(char in field.data for char in '!@#$%^&*()_+-=[]{};:\'",.<>/?`~\\'):
        raise ValidationError('Password must contain a special character')

def password_contains_capital(form, field):
    if not any(char.isupper() for char in field.data):
        raise ValidationError('Password must contain a capital letter')

def password_contains_number(form, field):
    if not any(char.isdigit() for char in field.data):
        raise ValidationError('Password must contain a number')

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
        Email(),
        validate_email_domain
    ])
    # NOTE: Maybe implement secure passwords?
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        password_contains_number
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

# TODO: Implement this correctly
class UpdateForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=1, max=30)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), validate_email_domain])
    submit = SubmitField('Update')

class SearchForm(FlaskForm):
    query = StringField('Search...', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Submit')