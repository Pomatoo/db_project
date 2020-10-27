from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# __init__ is where we initialize our application and components
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/testDB'
db = SQLAlchemy(app)
