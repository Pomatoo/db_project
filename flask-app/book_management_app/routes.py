import random
import time

from flask import request, render_template, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user, login_required

from book_management_app import app, db, login_manager
from book_management_app.forms import *
from book_management_app.models import Review



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""
1.Home Page will display all books, books are split into different pages
2.Select a random ASIN for "I'm Feeling Lucky"
3.Handle Search form
4.When user click on a book, it will redirect to book details (including reviews of this book) page
"""
@app.route("/", defaults={'page_num': 1, 'page_size': 12}, methods=['GET', 'POST'])
@app.route("/<page_num>/<page_size>", methods=['GET', 'POST'])
def home(page_size, page_num):
    mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              'Request': request.method, 'Path': request.full_path, 'Response': 200})

    # Select a random ASIN from database, this ASIN will be returned when user click "Lucky" button
    random_book_asin = mongo.db.book_meta.find().skip(random.randint(0, 434702)).limit(1)[0]['asin']

    # Pagination
    page_num = int(page_num)
    page_size = int(page_size)
    page_numbers = list(range(1, 36300))
    skips = page_size * (page_num - 1)
    book_meta = mongo.db.book_meta.find().skip(skips).limit(page_size)

    book_list = []
    for book in book_meta:
        book_list.append(book)

    form = SearchForm()
    if form.validate_on_submit():
        if form.type.data.lower() == 'asin':
            mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                      'Request': request.method, 'Path': request.full_path, 'Response': 302})
            return redirect(url_for('reviews', asin=form.keyword.data))
        elif form.type.data.lower() == 'book':
            # Find asin of the book then redirect to reviews page
            book_meta = mongo.db.book_meta.find_one({'title': form.keyword.data})
            if book_meta:
                mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                          'Request': request.method, 'Path': request.full_path, 'Response': 302})
                return redirect(url_for('reviews', asin=book_meta['asin']))
            else:
                flash('Book %s not found' % form.keyword.data, 'danger')
                return render_template('403.html')
    return render_template('home.html', form=form, books=book_list, page_numbers=page_numbers, page_size=page_size,
                           page_num=page_num, asin=random_book_asin)


@app.route("/about", methods=['GET'])
def about():
    mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              'Request': request.method, 'Path': request.full_path, 'Response': 200})
    return render_template('about.html')


"""
1. Book management page is open to admin only
2. Book management display all books, including pagination
3. When Admin click on a book, it will redirect to Edit Book page
"""
@app.route("/management", defaults={'page_num': 1, 'page_size': 12}, methods=['GET', 'POST'])
@app.route("/management/<page_num>/<page_size>", methods=['GET', 'POST'])
@login_required
def management(page_size, page_num):
    # Only Admin is allowed in book management page
    if current_user.username != 'admin':
        return redirect(url_for('home'))
    mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              'Request': request.method, 'Path': request.full_path, 'Response': 200})
    # Pagination
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
            return redirect(url_for('edit_book', asin=form.keyword.data))
        elif form.type.data.lower() == 'book':
            book_meta = mongo.db.book_meta.find_one({'title': form.keyword.data})
            mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                      'Request': request.method, 'Path': request.full_path, 'Response': 302})
            if book_meta:
                return redirect(url_for('edit_book', asin=book_meta['asin']))
            else:
                flash('Book %s not found' % form.keyword.data, 'danger')
                return render_template('403.html')
    return render_template('management.html', form=form, books=book_list, page_numbers=page_numbers,
                           page_size=page_size,
                           page_num=page_num)


"""
User registration page
"""
@app.route("/register", methods=['GET', 'POST'])
def register():
    # Only allow register when no user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              'Request': request.method, 'Path': request.full_path, 'Response': 200})
    if form.validate_on_submit():
        user = User(user_id=form.user_id.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                  'Request': request.method, 'Path': request.full_path, 'Response': 302})
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

"""
User login page
"""
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              'Request': request.method, 'Path': request.full_path, 'Response': 200})
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                      'Request': request.method, 'Path': request.full_path, 'Response': 302})
            return redirect(url_for('home'))
        else:
            mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                      'Request': request.method, 'Path': request.full_path, 'Response': 200})
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              'Request': request.method, 'Path': request.full_path, 'Response': 302})
    return redirect(url_for('home'))

"""
1. Add Book page is open to Admin only
2. Only new book can be added and all data fields must be filled
"""
@app.route("/add_book", methods=['GET', 'POST'])
@login_required
def add_book():
    # Only Admin is allowed in add book page
    if current_user.username != 'admin':
        return redirect(url_for('home'))

    form = AddBookForm()
    mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              'Request': request.method, 'Path': request.full_path, 'Response': 200})
    if form.validate_on_submit():
        try:
            mongo.db.book_meta.insert({'asin': form.asin.data, 'title': form.title.data,
                                       'price': form.price.data, 'description': form.description.data,
                                       'imUrl': form.image_url.data, 'categories': [],
                                       'related': {'also_bought': [], 'buy_after_review': []}
                                       })
        except:
            flash('Unable to add Book %s.' % form.asin.data, 'danger')
        else:
            flash('Book %s added successfully.' % form.asin.data, 'success')
            mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                      'Request': request.method, 'Path': request.full_path, 'Response': 302})
        finally:
            return redirect(url_for('management'))

    return render_template('add_book.html', title='Add Book', form=form, legend='Add Book')

"""
1. Display all reviews related to the book
2. ASIN is required to get to this page
"""
@app.route("/review/<asin>", methods=['GET', 'POST'])
def reviews(asin):
    book_meta = mongo.db.book_meta.find_one({'asin': asin})
    mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              'Request': request.method, 'Path': request.full_path, 'Response': 200})
    if book_meta:
        if 'related' in book_meta.keys():
            if 'also_viewed' not in book_meta['related'].keys():

                pass
                # print(book_meta)
                # review_list = Review.query.filter_by(asin=asin).all()
                # print('reviews size : %s ' % len(review_list))
                # print(review_list)
                # return render_template('review.html', title='Review', bookmeta=book_meta, reviews=review_list)
            else:
                book_meta['related']['also viewed'] = {}
                # review_list = Review.query.filter_by(asin=asin).all()
                # return render_template('review.html', title='Review', bookmeta=book_meta, reviews=review_list)
            # if 'related' in book_meta.keys():
            if 'buy_after_viewing' in book_meta['related']:
                pass
                # print(book_meta)
                # review_list = Review.query.filter_by(asin=asin).all()
                # print('reviews size : %s ' % len(review_list))
                # print(review_list)
                # return render_template('review.html', title='Review', bookmeta=book_meta, reviews=review_list)
            else:
                book_meta['related']['buy_after_viewing'] = {}
                # review_list = Review.query.filter_by(asin=asin).all()
                # return render_template('review.html', title='Review', bookmeta=book_meta, reviews=review_list)
        else:
            book_meta['related'] = {}
            # review_list = Review.query.filter_by(asin=asin).all()
        review_list = Review.query.filter_by(asin=asin).all()
        print('reviews size : %s ' % len(review_list))
        print(review_list)
        mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                  'Request': request.method, 'Path': request.full_path, 'Response': 200})
        return render_template('review.html', title='Review', bookmeta=book_meta, reviews=review_list)
    else:
        flash('Book %s not found' % asin, 'danger')
        return render_template('403.html')

"""
1. User can only post review after login

"""
@app.route("/add_review/<asin>", methods=['GET', 'POST'])
@login_required
def add_review(asin):
    form = AddReviewForm()
    if request.method == 'GET':
        book_meta = mongo.db.book_meta.find_one({'asin': asin})
        if book_meta:
            return render_template('add_review.html', title='Add Review', bookmeta=book_meta, form=form)
    mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              'Request': request.method, 'Path': request.full_path, 'Response': 200})
    if form.validate_on_submit():
        new_review = Review(
            asin=asin,
            helpful='%s' % [0, 0],
            overall=form.overall.data,
            review_text=form.review_text.data,
            review_time=time.strftime('%m %d, %y'),
            reviewer_id=current_user.user_id,
            reviewer_name=current_user.username,
            summary=form.summary.data,
            unix_review_time=int(time.time())
        )
        db.session.add(new_review)
        db.session.commit()
        mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                  'Request': request.method, 'Path': request.full_path, 'Response': 302})
        flash('Dear %s, your review to %s is added successfully.' % (current_user.username, asin), 'success')
        return redirect(url_for('reviews', asin=asin))


@app.route("/edit_book/<asin>", methods=['GET', 'POST'])
def edit_book(asin):
    form = EditBookForm()
    mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              'Request': request.method, 'Path': request.full_path, 'Response': 200})
    if request.method == "GET":
        book_meta = mongo.db.book_meta.find_one({'asin': asin})
        if book_meta:
            # Display existing parameters from database
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

        mongo.db.web_logs.insert({'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                  'Request': request.method, 'Path': request.full_path, 'Response': 302})
        return redirect(url_for('management'))


@app.route('/test')
@login_required
def test():
    return "<h1>test</h1>"
