const cv = require('opencv4nodejs'),
      jsfeat = require('jsfeat');
"use strict";

/*
    Description: a class to deal with stitching images together and handling overlap of the images.
*/
class Stitching {

    constructor(){

    }

    /*
        Description: a function for creating potential maps of a collection of images.
        @param imageArray - an array of image objects.
        @return an array of the image maps of the imageArray.
    */
    createImageMaps(imageArray){
        console.log("creating image map");
    }
}

module.exports = Stitching;