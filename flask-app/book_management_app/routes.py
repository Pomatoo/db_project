from book_management_app import app, db, mongo, bcrypt, login_manager
from book_management_app.models import Review, User
from book_management_app.forms import *
from flask import request, render_template, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user, login_required
from book_management_app.utils import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", defaults={'page_num': 1, 'page_size': 12})
@app.route("/<page_num>/<page_size>", methods=['GET', 'POST'])
def home(page_size, page_num):
    page_num = int(page_num)
    page_size = int(page_size)
    page_numbers = list(range(1, 4000))
    skips = page_size * (page_num - 1)
    book_meta = mongo.db.book_meta.find().skip(skips).limit(page_size)
    book_list = []
    for book in book_meta:
        book_list.append(book)

    form = SearchForm()
    if form.validate_on_submit():
        if form.type.data.lower() == 'asin':
            return redirect(url_for('reviews', asin=form.keyword.data))
        elif form.type.data.lower() == 'book':
            # Find asin of the book then redirect to reviews page
            book_meta = mongo.db.book_meta.find_one({'title': form.keyword.data})
            if book_meta:
                return redirect(url_for('reviews', asin=book_meta['asin']))
            else:
                flash('Book %s not found' % form.keyword.data, 'danger')

    return render_template('home.html', form=form, books=book_list, page_numbers=page_numbers, page_size=page_size,
                           page_num=page_num, catagories=[1, 2, 3, 4, 5])


@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')


@app.route("/management", defaults={'page_num': 1, 'page_size': 12}, methods=['GET', 'POST'])
@app.route("/management/<page_num>/<page_size>", methods=['GET', 'POST'])
@login_required
def management(page_size, page_num):

    if current_user.username != 'admin':
        return redirect(url_for('home'))

    form = SearchForm()
    page_num = int(page_num)
    page_size = int(page_size)
    page_numbers = list(range(1, 4000))
    skips = page_size * (page_num - 1)
    book_meta = mongo.db.book_meta.find().skip(skips).limit(page_size)
    book_list = []
    for book in book_meta:
        book_list.append(book)

    if form.validate_on_submit():
        if form.type.data.lower() == 'asin':
            return redirect(url_for('edit_book', asin=form.keyword.data))
        elif form.type.data.lower() == 'book':
            book_meta = mongo.db.book_meta.find_one({'title': form.keyword.data})
            if book_meta:
                return redirect(url_for('edit_book', asin=book_meta['asin']))
            else:
                flash('Book %s not found' % form.keyword.data, 'danger')

    return render_template('management.html', form=form, books=book_list, page_numbers=page_numbers,
                           page_size=page_size,
                           page_num=page_num)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_id=form.user_id.data, username=form.username.data, password=form.password.data)
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
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/add_book", methods=['GET', 'POST'])
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        mongo.db.book_meta.insert({'asin': form.asin.data, 'title': form.title.data,
                                   'price': form.price.data, 'description': form.description.data,
                                   'imUrl': form.image_url.data})
        flash('Book %s added successfully.' % form.asin.data, 'success')
        return redirect(url_for('management'))

    return render_template('add_book.html', title='Add Book', form=form, legend='Add Book')


@app.route("/review/<asin>", methods=['GET', 'POST'])
def reviews(asin):
    book_meta = mongo.db.book_meta.find_one({'asin': asin})
    if book_meta:
        print(book_meta)
        review_list = Review.query.filter_by(asin=asin).all()
        print('reviews size : %s ' % len(review_list))
        for i in review_list:
            print(i.review_text)
        return render_template('review.html', title='Review', bookmeta=book_meta, reviews=review_list)
    else:
        flash('Book %s not found' % asin, 'danger')
        return render_template('403.html')


@app.route("/add_review/<asin>", methods=['GET', 'POST'])
@login_required
def add_review(asin):
    form = AddReviewForm()
    if request.method == 'GET':
        book_meta = mongo.db.book_meta.find_one({'asin': asin})
        if book_meta:
            return render_template('add_review.html', title='Add Review', bookmeta=book_meta, form=form)

    if form.validate_on_submit():
        print(asin)
        print(current_user.username)
        print(current_user.user_id)
        print(form)
        return redirect(url_for('reviews'))

    return "<h1>add review</h1>"


@app.route("/edit_book/<asin>", methods=['GET', 'POST'])
def edit_book(asin):
    form = EditBookForm()
    if request.method == "GET":
        book_meta = mongo.db.book_meta.find_one({'asin': asin})
        if book_meta:
            # This Block is dumb but I cant write better code :(
            if 'asin' in book_meta.keys():
                form.asin.data = book_meta['asin']
            if 'title' in book_meta.keys():
                form.title.data = book_meta['title']
            if 'price' in book_meta.keys():
                form.price.data = book_meta['price']
            if 'description' in book_meta.keys():
                form.description.data = book_meta['description']
            if 'imUrl' in book_meta.keys():
                form.image_url.data = book_meta['imUrl']
            return render_template('edit_book.html', title='Edit Book', form=form, legend='Edit Book', book=book_meta)
        else:
            flash('Book %s not found' % asin, 'danger')
            return render_template('403.html')

    if form.is_submitted():
        mongo.db.book_meta.update_one({'asin': asin}, {"$set": {'asin': form.asin.data, 'title': form.title.data,
                                                                'price': form.price.data,
                                                                'description': form.description.data,
                                                                'imUrl': form.image_url.data}})
        a = mongo.db.book_meta.find({'asin': asin})
        return redirect(url_for('management'))


@app.route('/test')
@login_required
def test():
    return "<h1>test</h1>"


# {"user_id":"", "HTTP_METHOD":"", "RESOURCE":""}

