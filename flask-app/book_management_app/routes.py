from book_management_app import app, db, bcrypt, login_manager, mongo
from book_management_app.models import Review, User
from book_management_app.forms import RegistrationForm, LoginForm, SearchForm
from flask import request, render_template, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user, login_required


# /review [GET, POST] -> Retrieve review,  post a review

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", defaults={'page_num': 1, 'page_size': 12})
@app.route("/<page_num>/<page_size>", methods=['GET', 'POST'])
def home(page_size, page_num):
    form = SearchForm()
    page_num = int(page_num)
    page_size = int(page_size)
    page_numbers = list(range(1, 4000))
    skips = page_size * (page_num - 1)
    book_meta = mongo.db.book_meta.find().skip(skips).limit(page_size)
    # i = 0
    book_list = []
    for book in book_meta:
        #     i += 1
        #     if i == 10:
        #         break
        book_list.append(book)

    if form.validate_on_submit():
        print(form.keyword.data)
        print(form.type.data)

        if form.type.data.lower() == 'asin':

            book_meta = mongo.db.book_meta.find_one({'asin': form.keyword.data})
            if book_meta:
                print(book_meta)
                reviews = Review.query.filter_by(asin=form.keyword.data).all()
                print(type(reviews))
                print('reviews size : %s ' % len(reviews))
                for i in reviews:
                    print(reviews)
            else:
                flash('Book %s not found' % form.keyword.data, 'danger')
        elif form.type.data.lower() == 'book':
            pass

    return render_template('home.html', form=form, books=book_list, page_numbers=page_numbers, page_size=page_size,
                           page_num=page_num)


@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')


@app.route("/management", methods=['GET'])
@login_required
def management():
    if current_user.username == 'admin':
        book_meta = mongo.db.book_meta.find()
        book_list = []
        for book in book_meta:
            book_list.append(book)
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


@app.route("/book/<asin>")
def book(asin):
    book_meta = mongo.db.book_meta.find()
    book_list = []
    for book in book_meta:
        book_list.append(book)
        return render_template('book.html', title='book', book_list=book_list)
