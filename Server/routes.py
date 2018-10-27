from . import app
from flask import render_template, send_from_directory, request, url_for, redirect
from werkzeug.utils import secure_filename
from lib.counting import *
from lib.stitching import *
import os
import datetime

ALLOWED_IMAGE_EXTENSIONS = set(['jpg', 'jpeg'])
ALLOWED_VIDEO_EXTENSIONS = set(['mp4'])

"""
    Description: a function used to see if the uploaded file is in a valid format.
    @Param filename - name of the file being uploaded.
    @Param extensionList - set of allowed file extensions.
    @return a boolean indicating whether the image is in an acceptable format or not.
"""
def isFileAllowed(filename, extensionList):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensionList

def setupUploadDir():
    # create new folder to hold users data for run
    uploadDir = './Server/resources/uploads'
    now = datetime.datetime.now()
    newFolder = now.strftime("%Y-%m-%dT%H_%M_%S")
    newDir = uploadDir + "/" + newFolder
    os.mkdir(newDir)
    subfolders = ['images', 'videos', 'maps', 'results']
    for folder in subfolders:
        subDir = newDir + "/" + folder
        os.mkdir(subDir)
    return newDir

# route for serving static resources (images/js/css)
@app.route('/resources/<path:path>')
def sendJs(path):
    return send_from_directory('resources', path)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/error')
def error():
    errorMessage = request.args['errorMessage']
    return render_template('error.html',error=errorMessage)

@app.route('/uploadImages', methods=["POST"])
def uploadImages(): 
    images = request.files.getlist("images")
    magLevel = request.form["magLevel"]

    newDir = setupUploadDir()

    for i in images: 
        #redirect to error page if the image is in an unacceptable
        if(isFileAllowed(i.filename,ALLOWED_IMAGE_EXTENSIONS) == False): 
            return redirect(url_for('error',errorMessage="One or more of the images that were uploaded are in the incorrect format. Accepted formats: "+(", ".join(ALLOWED_IMAGE_EXTENSIONS))))

        print("Image is permitted: "+str(isFileAllowed(i.filename,ALLOWED_IMAGE_EXTENSIONS))) #see if the image format is allowed
        print("Secure filename: "+str(secure_filename(i.filename))) #escape the filename

        imgPath = newDir + "/images/" + str(secure_filename(i.filename))
        i.save(imgPath)
    

    #TODO: return location of the directory to the user
    return redirect(url_for('index')) #redirect to homepage

@app.route('/uploadVideo', methods=["POST"])
def uploadVideo(): 
    video = request.files['video']

    newDir = setupUploadDir()

    #redirect to the error page if the video is not the correct format
    if(isFileAllowed(video.filename,ALLOWED_VIDEO_EXTENSIONS) == False):
        return redirect(url_for('error',errorMessage="The uploaded video is in the incorrect format. Accepted formats: "+(", ".join(ALLOWED_VIDEO_EXTENSIONS))))

    print("Video is permitted: "+str(isFileAllowed(video.filename,ALLOWED_VIDEO_EXTENSIONS))) #see if the image format is allowed
    print("Secure filename: "+str(secure_filename(video.filename))) #escape the filename

    # place video in a unique directory
    vidPath = newDir + "/videos/" + str(secure_filename(video.filename))
    video.save(vidPath)
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

# accepts a path to the stitched image directory
@app.route('/getResults/<path:directory>')
def getResults(directory): 
    print("getting getResults")
    print(directory)
    results = ""
    #TODO: format results from bead counting 
    #TODO: return results and store them locally

    count = Counting(directory)
    #TODO: add logic here for config
    circles = count.getColorBeads(HoughConfig.OBJX10)
    results += "Valid beads: " + str(len(circles))
    results += "/n" + "Water beads: " + str(len(count.waterBeads))

    return results 
