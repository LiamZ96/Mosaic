# Mosaic

# Description
Microbead detecting software written for CSC-450. Intended to stitch together images provided by user and count the total number of microbeads.

# Installation Instructions
* Start your preferred shell (may need to start as an administrator). Make sure you have cmake >= 3.7 installed and it is in your path https://cmake.org/download/).
* Globally install windows build tools. run "npm install -g windows-build-tools". This is needed to compile the opencv library which is what opencv4nodejs will do when installing it.
* Run "npm install" to install all dependencies (this might take a while to compile opencv for opencv4nodejs. It took me around 8 minutes).

# Pull Request Instructions
TBD

# Code Standards 
* All functions should have a docstring consisting of description, parameters, and return value in the format of javadocs.
* Private methods in classes should start with an underscore character.
* Functions and variable names will be in camel case format.
* Functions that don't fit on the screen should be split into multiple functions.
* Each javascript file will start with "use strict". 
* Let and const will be used over var for variable declarations.