from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from book_management_app.models import User
from book_management_app import mongo

"""
Flask Forms
"""


class RegistrationForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_user_id(self, user_id):
        user = User.query.filter_by(user_id=user_id.data).first()
        if user:
            raise ValidationError('That user ID is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired(), Length(min=1, max=100)])
    type = SelectField('Type', choices=['ASIN', 'Book'])
    submit = SubmitField('Search')


class AddReviewForm(FlaskForm):
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(min=1, max=100)])
    overall = SelectField('Overall Rating', choices=['5', '4', '3', '2', '1'])
    review_text = TextAreaField('Review', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Add Review')


class AddBookForm(FlaskForm):
    asin = StringField('ASIN', validators=[DataRequired(), Length(min=1, max=100)])
    title = StringField('Title', validators=[Length(min=1, max=200)])
    price = StringField('Price', validators=[Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[Length(min=1, max=5000)])
    image_url = StringField('ImageURL', validators=[Length(min=1, max=1000)])
    submit = SubmitField('Add Book')

    def validate_asin(self, asin):
        book_meta = mongo.db.book_meta.find_one({'asin': asin.data})
        if book_meta:
            raise ValidationError('That ASIN exist. Please choose a different one.')


class EditBookForm(FlaskForm):
    asin = StringField('ASIN', validators=[DataRequired(), Length(min=1, max=100)])
    title = StringField('Title', validators=[Length(min=1, max=100)])
    price = StringField('Price', validators=[Length(min=1, max=100)])
    description = StringField('Description', validators=[Length(min=1, max=100)])
    image_url = StringField('ImageURL', validators=[Length(min=1, max=100)])
    submit = SubmitField('Apply')
