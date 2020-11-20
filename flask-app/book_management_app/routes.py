from book_management_app import app, db, mongo, bcrypt, login_manager
from book_management_app.models import Review, User, Book
from book_management_app.forms import RegistrationForm, LoginForm, SearchForm, addBookForm
from flask import request, render_template, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user, login_required


# /review [GET, POST] -> Retrieve review,  post a review

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    book_meta = mongo.db.book_meta.find()
    i = 0
    books_list = []
    for book in book_meta:
        i += 1
        if i == 10:
            break
        print(book)
        books_list.append(book)

    if form.validate_on_submit():
        print(form.keyword.data)
        print(form.type.data)
        if form.type.data.lower() == 'asin':
            book_meta1 = mongo.db.book_meta.find_one({'asin': form.keyword.data})
            print('Book meta %s ' % book_meta1)
            if book_meta1:
                print(book_meta1)
                reviews = Review.query.filter_by(asin=form.keyword.data).all()
                print(type(reviews))
                print('reviews size : %s ' % len(reviews))
                for i in reviews:
                    print(i.review_text)
                return redirect(url_for('reviews'))
            else:
                flash('Book %s not found' % form.keyword.data, 'danger')
        elif form.type.data.lower() == 'book':
            pass

    return render_template('home.html', form=form, books=books_list)


@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')


@app.route("/management", methods=['GET'])
@login_required
def management():
    if current_user.username == 'admin':

        return render_template('management.html')
    else:
        flash('Please login as admin and try again', 'danger')
        return render_template('403.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('management'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/addbook", methods=['GET', 'POST'])
def addbook():
    form = addBookForm()
    if form.validate_on_submit():
        print(form.asin.data)
        print(form.Title.data)
        mongo.db.book_meta.insert({'asin': form.asin.data, 'title': form.Title.data,
                                   'price': form.Price.data, 'description': form.Description.data,
                                   'imUrl': form.ImageURL.data})
        return redirect(url_for('home'))
    else:
        print("Add book failed")

    return render_template('add-book.html', title='Add Book', form=form)


@app.route("/review/<asin>", methods=['GET', 'POST'])
def reviews(asin):
    book_meta1 = mongo.db.book_meta.find_one({'asin': asin})
    print('Book meta %s ' % book_meta1)
    if book_meta1:
        print(book_meta1)
        review = Review.query.filter_by(asin=asin).all()
        print(type(review))
        print('reviews size : %s ' % len(review))

        for i in review:
            print(i.review_text)



    return render_template('review.html', title='Review', bookmeta=book_meta1, reviews=review)
