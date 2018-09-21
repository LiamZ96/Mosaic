const cv = require('opencv4nodejs'),
      jsfeat = require('jsfeat');
"use strict";

/*
    Description: a class to deal with counting microbeads in a stitched image.
*/
class Counting {

    constructor(){

    }

    /*
        Description: a function that takes a map of images and counts the beads.
        @param imageMap - a map (image) of the microscope images.
        @return an object containing information collected during the counting process.
    */
    countBeads(imageMap){
        console.log("counting beads");
    }
}

module.exports = Counting;