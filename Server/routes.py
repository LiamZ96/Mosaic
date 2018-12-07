'''
MIT License

Copyright (c) 2018 LiamZ96

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
#Requirements in this file: 3.1.2, 3.1.4, 3.1.5, 3.1.11, 3.2.7, 3.3.2
#Authors: Jacob Wakefield, Noah Zeilmann, McKenna Gates, Liam Zay

from . import app
from flask import render_template, send_from_directory, request, url_for, redirect, jsonify
from werkzeug.utils import secure_filename
from lib.counting import *
from lib.stitching import *
import os
import datetime
import json
from PIL import Image

ALLOWED_IMAGE_EXTENSIONS = set(['jpg', 'jpeg'])
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'avi'])

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
    uploadDir = 'Server/resources/uploads'
    now = datetime.datetime.now()
    newFolder = now.strftime("%Y-%m-%dT%H-%M-%S")
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

    newDir = setupUploadDir()

    for i in images: 
        #redirect to error page if the image is in an unacceptable
        if(isFileAllowed(i.filename,ALLOWED_IMAGE_EXTENSIONS) == False): 
            return jsonify({"status": 1, "msg": "One or more of the images that were uploaded are in the incorrect format. Accepted formats: "+(", ".join(ALLOWED_IMAGE_EXTENSIONS))})

        print("Image is permitted: "+str(isFileAllowed(i.filename,ALLOWED_IMAGE_EXTENSIONS))) #see if the image format is allowed
        print("Secure filename: "+str(secure_filename(i.filename))) #escape the filename

        imgPath = newDir + "/images/" + str(secure_filename(i.filename))
        i.save(imgPath)
    
    return jsonify({"status": 0, "msg": "Success","location": newDir.replace("Server/resources/uploads","")}) #redirect to homepage

@app.route('/uploadVideo', methods=["POST"])
def uploadVideo(): 
    video = request.files['video']

    newDir = setupUploadDir()

    #redirect to the error page if the video is not the correct format
    if(isFileAllowed(video.filename,ALLOWED_VIDEO_EXTENSIONS) == False):
        return jsonify({"status": 1, "msg": "The uploaded video is in the incorrect format. Accepted formats: "+(", ".join(ALLOWED_VIDEO_EXTENSIONS))})

    print("Video is permitted: "+str(isFileAllowed(video.filename,ALLOWED_VIDEO_EXTENSIONS))) #see if the image format is allowed
    print("Secure filename: "+str(secure_filename(video.filename))) #escape the filename

    # place video in a unique directory
    vidPath = newDir + "/videos/" + str(secure_filename(video.filename))
    video.save(vidPath)
    return jsonify({"status": 0, "msg": "Success"}) #redirect to homepage


# accepts a path to the image directory to use for stitching
@app.route('/getStitchedImage/<path:directory>')
def getStitchedImage(directory): 
    dirPrefix="Server/resources/uploads/"
    stitcher = Stitching()
    
    stitcher.twoRoundStitch(dirPrefix + directory + "/images/", dirPrefix + directory + "/maps/")
    return render_template('stitched.html', direct=directory)

# accepts a path to the stitched image directory
@app.route('/getResults/<path:directory>')
def getResults(directory): 
    magLevel = request.args.get('magLevel')
    if(magLevel == "4x"):
        magLevel = HoughConfig.OBJX4
    else: 
        magLevel = HoughConfig.OBJX10
    resultsDirectory = directory.split("/")[0]
    serverDirectory = 'Server/resources/uploads/' + directory
    count = Counting(serverDirectory)
    circles = count.getColorBeads(magLevel)
    count.makeBeadsCSV()
    return render_template('results.html',colorBeads=circles,waterBeads=count.waterBeads, mapLocation=directory, resultsDirectory=resultsDirectory) 
