from sys import argv
from book_management_app import app
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

# Why import book_management_app? -> book_management_app is package
'''
Tree structure
├── book_management_app
│    ├── __init__.py
│    ├── models.py
│    ├── routes.py
│    └── test.py
└── run.py
'''

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8080
    if len(argv) == 2 and argv[1] == 'deploy':
        HOST = '0.0.0.0'

    app.run(host=HOST, port=PORT, debug=True)
