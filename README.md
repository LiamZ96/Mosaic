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

# Mosaic

# Description
Microbead detecting software written for CSC-450. Intended to stitch together images provided by user and count the total number of microbeads.

# Installation Instructions
* To download python packages ensure you have the latest version of python3 installed, and that you have it in your path. Then in the command prompt navigate to where you have mosaic installed, and run this command "python -m pip install -r requirements.txt". 
* To install .js dependencies ensure you have npm installed and run "npm install".

#Running the server
Use these commands for window's command prompt. Other OSs' may require different commands
* set FLASK_APP=Server
* set FLASK_ENV=development  
* py -m flask run

# Pull Request Instructions
* Open a pull request into master with a clear description of what was changed and why.
* The pull request will then be reviewed and approved by at least 4 of the 6 collaborators.
* Once approved the branch will be merged with master. 
* If the branch being merged with master was a feature branch, it will be deleted.

# Code Standards 
* All functions should have a docstring consisting of description, parameters, and return value in the format of javadocs.
* Private methods in classes should start with an underscore character.
* Functions and variable names will be in camel case format.
* Functions that don't fit on the screen should be split into multiple functions.
* Each javascript file will start with "use strict". 
* Let and const will be used over var for variable declarations.
