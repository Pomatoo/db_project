from book_management_app import db


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
