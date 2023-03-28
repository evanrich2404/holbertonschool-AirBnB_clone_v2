#!/usr/bin/python3
"""starts a Flask web application that displays a state"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """displays a HTML page with a list of states"""
    states = storage.all("State")
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """displays a HTML page with a list of states"""
    for state in storage.all("State").values():
        if state.id == id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html')


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
