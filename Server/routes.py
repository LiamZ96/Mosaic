from . import app
from flask import render_template, send_from_directory, request, url_for, redirect
from werkzeug.utils import secure_filename

ALLOWED_FILE_EXTENSIONS = set(['jpg', 'jpeg', 'mp4'])

"""
    Description: a function used to see if the uploaded file is in a valid format.
    @Param filename - name of the file being uploaded.
"""
def isFileAllowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

# route for serving static resources (images/js/css)
@app.route('/resources/<path:path>')
def sendJs(path):
    return send_from_directory('resources', path)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/uploadImages', methods=["POST"])
def uploadImages(): 
    images = request.files.getlist("images")
    for i in images: 
        print("Image is permitted: "+str(isFileAllowed(i.filename))) #see if the image format is allowed
        print("Secure filename: "+str(secure_filename(i.filename))) #escape the filename
    return redirect(url_for('index')) #redirect to homepage