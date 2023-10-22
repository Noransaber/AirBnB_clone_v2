#!/usr/bin/python3
"""
Web Flask Application
"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
	Displaying a HTML page with states orderd alphabetically
	"""
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """Storage Close"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')