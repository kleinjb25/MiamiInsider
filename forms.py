
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea
import email_validator

stop_words = ['a', 'an', 'the', 'and', 'but', 'or', 'if', 'because', 'as', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under']

def validate_search_common_words(form, field):
    query = field.data
    if query in stop_words: # Check if search query is common/unspecific word
        raise ValidationError('This word will not provide an accurate search result.')

def validate_email_domain(form, field):
    email = field.data
    domain = email.split('@')[1] # Get the domain from the email
    if domain != 'miamioh.edu': # Check if domain is not miamioh.edu
        raise ValidationError('Email must be of @miamioh.edu domain')

def validate_phone_number(form, field):
    # Using regex to validate phone number format
    import re
    pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
    if field.data != 'None' and not re.match(pattern, field.data):
        raise ValidationError('Invalid phone number format. Format should be (XXX) XXX-XXXX')

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

class UpdateForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=1, max=30)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), validate_email_domain])
    phone = StringField('Phone', validators=[DataRequired(), validate_phone_number])
    private = BooleanField('Keep profile private')
    submit = SubmitField('Update')

class SearchForm(FlaskForm):
    query = StringField('Search...', validators=[DataRequired(), Length(min=2)])
    sort = HiddenField('Sort Value')
    # TODO: Category
    # TODO: Sorting
    submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
    rating = HiddenField(validators=[DataRequired()])
    text = StringField('Text...', widget=TextArea(), validators=[Length(max=250)])
    submit = SubmitField('Review')
