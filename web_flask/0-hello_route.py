#!/usr/bin/python3
from flask import Flask

# Starting the application
app = Flask(__name__)

# Routing to the path '/'
@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"

# Make it listen to other machines
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
