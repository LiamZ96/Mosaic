const Stitching = require("./lib/stitching.js"),
      Counting = require("./lib/counting.js");
"use strict";

let stitch = new Stitching();
let count = new Counting();

stitch.createImageMaps(null);
count.countBeads(null);
