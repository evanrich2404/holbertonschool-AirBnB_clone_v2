#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from markupsafe import escape


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """display Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """display HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """display C followed by the value of the text variable"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/', defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """display Python followed by the value of the text variable"""
    if text is None or text == '':
        text = 'is_cool'
    else:
        return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """display n is a number only if n is an integer"""
    if isinstance(n, int):
        return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """display a HTML page only if n is an integer"""
    if isinstance(n, int):
        return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
