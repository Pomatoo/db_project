# db_project
1. Automation script: (in progress)
    - create instances 
    - attach security group 
    - sh script to install packages and setup configuration (MySQL,MongoDB)
    - load dataset from get_data.sh

2. Production System:
    1 - UI/UX (in progress)
    1 - Flask web (in progress)

3. Analytics System 
    - No progress yet


A front-end with at least the following functionalities:
    Add a new book
    Search for existing book by author and by title.
    Add a new review
    Sort books by reviews(# of reviews/ rating), genres.
    ## Additional features
    Bookmark/Favorite 
    I'm Feeling Lucky -> Suggest a book 

API
1# domain/signup [GET, POST] -> Sign up
1# /login [GET,POST] -> Login

0.5# /home [GET] -> Home page, display top rated books
# /book [GET, POST] -> Add a book -{asin,author,price .. }, search/get a book {asin,tile}

# /review [GET, POST] -> Retrieve review,  post a review

# For HTTP GET method -> parameters are passed via variables in URL, should not have body for GET
# POST -> Data is passed using Form Obj in flask 


Questions for Profs:
Login credentials, ssh key to instance (auto)?
Instances specs /InstanceType(IMG id) is restricted
Python libs: SqlAlchemy -  ORM framework allowed? 
any changes on dataset during demo/grading?
Add a new book (what parameters are required? ASIN, Author, Price)
Sort by view based on rating? how about genres ?


