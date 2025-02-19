#!/usr/bin/python3
""" starts a Flask web application """
from models import storage
from flask import Flask, render_template
from models.state import State, Amenity

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """ displays a HTML page with a list of states """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """ closes the storage on teardown """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
