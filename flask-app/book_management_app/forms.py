from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from book_management_app.models import User
from book_management_app import mongo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    '''
    Any methods with method name: validate_%s will be evoked when Form.validate_on_submit() is called
    '''

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired(), Length(min=1, max=100)])
    type = SelectField('Type', choices=['ASIN', 'Book'])
    submit = SubmitField('Search')


class addBookForm(FlaskForm):
    asin = StringField('ASIN', validators=[DataRequired(), Length(min=1, max=100)])
    Title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    Price = StringField('Price', validators=[DataRequired(), Length(min=1, max=100)])
    Description = StringField('Description', validators=[DataRequired(), Length(min=1, max=100)])
    ImageURL = StringField('ImageURL', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('AddBook')

    def validate_asin(self, asin):
        book_meta = mongo.db.book_meta.find_one({'asin': asin})
        if not book_meta:
            raise ValidationError('That ASIN exist. Please choose a different one.')
