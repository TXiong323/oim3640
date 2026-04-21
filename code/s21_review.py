"""
Session 21 Review (4/09)
Topic: Introduction to Flask - routes, templates, forms, POST requests

This file collects the Python code from the Session 21 slides.
HTML templates are included as comments for reference.

To actually run any of these, put the Python part in app.py
and the HTML parts in a templates/ folder next to it.
"""

from flask import Flask, render_template, request


# ============================================================
# Your First Flask App
# ============================================================

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)

# Terminal:
#   cd helloflask
#   pip install flask
#   python app.py
# Visit http://127.0.0.1:5000


# ============================================================
# More Routes - URL parameters
# ============================================================

@app.route('/hello/<name>')
def hello_name(name):
    return f'Hello, {name}!'
# Visit /hello/Zhi  --> "Hello, Zhi!"


@app.route('/square/<int:n>')
def square(n):
    return f'{n} squared is {n ** 2}'
# Visit /square/7  --> "7 squared is 49"


# ============================================================
# Flask Templates (Jinja)
# ============================================================

@app.route('/hello/<name>')
def greet(name):
    return render_template('hello.html', name=name)


# templates/hello.html:
# <h1>Hello, {{ name }}!</h1>
# <p>Welcome to my Flask app.</p>


# ============================================================
# HTML Forms - send data to Flask
# ============================================================

# templates/form_example.html:
# <form method="POST" action="/search">
#     <label>Enter a place:</label>
#     <input type="text" name="place">
#     <button type="submit">Search</button>
# </form>
#
# method="POST"     -- sends data in the request body (not URL)
# action="/search"  -- where to send the form data
# name="place"      -- the key used to read the input in Python


# ============================================================
# Handling Form Submissions
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    place = request.form['place']
    return render_template('result.html', place=place)


# templates/index.html:
# <h1>Place Search</h1>
# <form method="POST" action="/search">
#     <input type="text" name="place" placeholder="e.g., Boston Common">
#     <button type="submit">Search</button>
# </form>
#
# templates/result.html:
# <h1>Results for {{ place }}</h1>
# <p>You searched for: {{ place }}</p>
# <a href="/">Search again</a>


# ============================================================
# Template Inheritance
# ============================================================

# templates/base.html:
# <html>
# <head><title>My App</title></head>
# <body>
#     <nav><a href="/">Home</a></nav>
#     {% block content %}{% endblock %}
# </body>
# </html>
#
# templates/index.html:
# {% extends "base.html" %}
# {% block content %}
# <h1>Welcome!</h1>
# {% endblock %}


# ============================================================
# Flask Project Structure
# ============================================================

# myapp/
# ├── app.py              # routes and logic
# ├── mbta_helper.py      # API helper functions
# ├── .env                # API keys (never commit!)
# ├── .gitignore          # includes .env
# ├── templates/
# │   ├── base.html       # shared layout
# │   ├── index.html      # home page with form
# │   └── result.html     # results page
# └── static/
#     └── style.css       # optional CSS


# ============================================================
# MP3: nearest MBTA station web app
# ============================================================

# 1. User enters a place name in a form
# 2. Call Mapbox API to get coordinates
# 3. Call MBTA API to find the nearest stop
# 4. Display the result (and optionally a map)
#
# Mapbox:  https://account.mapbox.com/auth/signup/
# MBTA:    https://api-v3.mbta.com