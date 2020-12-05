from book_management_app import db
from flask_login import UserMixin

"""
ORM for MySQL
"""


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(255), index=True, nullable=False)
    helpful = db.Column(db.String(255), nullable=False)
    overall = db.Column(db.String(255), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    review_time = db.Column(db.String(255), nullable=False)
    reviewer_id = db.Column(db.String(255), nullable=False)
    reviewer_name = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    unix_review_time = db.Column(db.Integer, nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(60), nullable=True)
