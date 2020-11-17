
from book_management_app import app

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
    PORT = 5000
    app.run(host=HOST, port=PORT, debug=True)
