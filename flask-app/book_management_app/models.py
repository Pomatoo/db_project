from book_management_app import db
from flask_login import UserMixin


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

    def __repr__(self):
        return (f"Review('{self.asin}', '{self.helpful}', '{self.overall}',"
                f"'{self.review_text}, '{self.review_time}, '{self.reviewer_id}, '{self.reviewer_name}"
                f", '{self.summary}), '{self.unix_review_time})")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"


class Book(object):
    asin = ''
    img_url = ''
    price = ''
    title = ''
    description = ''
