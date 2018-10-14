from . import app
import flask
from flask import render_template, send_from_directory, request

# route for serving static resources (images/js/css)
@app.route('/resources/<path:path>')
def send_js(path):
    return send_from_directory('resources', path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploadImages', methods=["POST"])
def uploadImages(): 
    images = request.files.getlist("images")
    print(images)
    return ""