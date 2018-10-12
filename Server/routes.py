from . import app
from flask import render_template, send_from_directory

# route for serving static resources (images/js/css)
@app.route('/resources/<path:path>')
def send_js(path):
    return send_from_directory('resources', path)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')