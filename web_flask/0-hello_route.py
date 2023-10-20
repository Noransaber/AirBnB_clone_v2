#!/usr/bin/python3
"""Starts a Flask web application:
/: display “Hello HBNB!”
"""
from flask import Flask

# Starting the application
app = Flask(__name__)


# Routing to the path '/'
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Return Hello HBNB"""
    return "Hello HBNB!"


# Make it listen to other machines
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
