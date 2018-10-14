from . import app
from flask import render_template, send_from_directory, request, url_for, redirect
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = set(['jpg', 'jpeg'])
ALLOWED_VIDEO_EXTENSIONS = set(['mp4'])

"""
    Description: a function used to see if the uploaded file is in a valid format.
    @Param filename - name of the file being uploaded.
    @Param extensionList - set of allowed file extensions.
"""
def isFileAllowed(filename, extensionList):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensionList

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
        print("Image is permitted: "+str(isFileAllowed(i.filename,ALLOWED_IMAGE_EXTENSIONS))) #see if the image format is allowed
        print("Secure filename: "+str(secure_filename(i.filename))) #escape the filename
    
    #TODO: place images in a unique directory 
    #TODO: return location of the directory to the user
    return redirect(url_for('index')) #redirect to homepage

@app.route('/uploadVideo', methods=["POST"])
def uploadVideo(): 
    video = request.files['video']

    print("Video is permitted: "+str(isFileAllowed(video.filename,ALLOWED_VIDEO_EXTENSIONS))) #see if the image format is allowed
    print("Secure filename: "+str(secure_filename(video.filename))) #escape the filename
    return redirect(url_for('index')) #redirect to homepage

# accepts a path to the image directory to use for stitching
@app.route('/getStitchedImage/<path:directory>')
def getStitchedImage(directory): 
    print("getting stiched image")
    print(directory)
    #TODO: start stitching process from a given directory
    #TODO: place stitched images into a directory within the image directory
    #TODO: return link to the stitched image
    return "" 