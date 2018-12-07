/*
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
*/

//Authors: Jacob Wakefield

var imageObj = undefined; //the stitched map image

    /*
        a function to draw a bead
        @param bead - the bead to be drawn. 
        @param ctx - the context of the canvas.
    */
   var drawBead = function(bead,ctx) {
        var x = bead[2][0],
            y = bead[2][1],
            radius = bead[2][2]/4; //TODO: translate this radius like the x,y
        ctx.beginPath();
        ctx.arc(x,y,radius,0,2*Math.PI);
        if(bead[1]){
            ctx.strokeStyle=$("#waterBeadOutline").val();
        }else{
            ctx.strokeStyle=$("#colorBeadOutline").val();
        }
        ctx.lineWidth=5;
        ctx.stroke();
    };

    /*
        a function to check if a point is within a circle.
        @param x - the x position to check
        @param y - the y position to check
        @param cx - the circle x position
        @param cy - the circle y position 
        @param radius - the radius of the circle
    */
    var pointInCircle = function(x, y, cx, cy, radius) {
        var dx = x - cx,
            dy = y - cy,
            dist = Math.sqrt(dx * dx + dy * dy);
        return dist < radius;
        
        // var distsq = (x-cx)*(x-cx) + (y-cy)*(y-cy);
        // return distsq <= radius*radius;
    };
    
    /*
    a function to handle the hover over the canvas. 
    @param clientX - the x position of the clients mouse. 
    @param clientY - the y position of the clients mouse.
    @param ctx - the canvas context.
    */
   var handleHover = function(clientX,clientY,ctx) {
       var allBeads = beads.colorBeads.concat(beads.waterBeads),
       toolTipBead = undefined;
       allBeads.forEach(function(bead){
           var x = bead[2][0],
               y = bead[2][1],
               radius = bead[2][2];
           if(pointInCircle(x,y,clientX,clientY,radius)){
               toolTipBead = bead;
            }
        });
        if(toolTipBead){
            var rectWidth = 300,
                rectHeight = 50,
                rectX = toolTipBead[2][0],
                rectY = toolTipBead[2][1];
            redraw(ctx);

            ctx.fillStyle = "white";
            ctx.fillRect(rectX,rectY,rectWidth,rectHeight);
            // draw font in red
            ctx.fillStyle = "black";
            ctx.font = "10pt sans-serif";
            var text = "RGB: ("+toolTipBead[0][0]+", "+toolTipBead[0][1]+", "+toolTipBead[0][2] + ")    isWater: "+toolTipBead[1];
        
            ctx.fillText(text,rectX+10,rectY+(rectHeight/2),rectX+rectWidth);
        }
    };

    /*
        a function to translate a x/y value into a new height/width of a canvas.
        @param coord - the coordinate to translate into a new range. 
        @param oldRange - old height/width.
        @param newRange - new height/width.
    */
    var translateCoord = function(coord,oldRange,newRange) {
        return ((coord*newRange) / oldRange);
    };
    
    /*
    a function used to translate the beads from the old image height/width to the new canvas height/width.
    @param beadArray - the bead array to translate 
    @param height - the new canvas height
    @param width - the new canvas width
    */
   var translateBeads = function(beadArray,height,width) {
       var newBeads = [];
       beadArray.forEach(function(bead){
           var newBead = [
               bead[0],
               bead[1],
            [translateCoord(bead[2][0],imageObj.width,width),translateCoord(bead[2][1],imageObj.height,height),bead[2][2]]
        ];
        newBeads.push(newBead);
    });
    return newBeads;
};

/*
    a function to clear and redraw the canvas.
    @param ctx - the context of the canvas
*/
var redraw = function(ctx) {
    ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);//clear the canvas before redrawing
    ctx.drawImage(imageObj,0,0,ctx.canvas.width,ctx.canvas.height); //draw the image first

    beads.colorBeads.forEach(function(bead){
        drawBead(bead,ctx);
    });
    beads.waterBeads.forEach(function(bead){
        drawBead(bead,ctx);
    });
};

$(window).ready(function() {
    var canvas = document.getElementById('mapCanvas'),
        canvasWrapper = $("#canvasWrapper"),
        ctx = canvas.getContext('2d'),
        height = canvasWrapper.height() * 2, //set the height based on the save of the canvas wrapper * 2
        width = canvasWrapper.width(); //set the width based on the save of the canvas wrapper
    imageObj = new Image();
    imageObj.src = mapLocation;
    ctx.canvas.width = width;
    ctx.canvas.height = height;
    
    imageObj.onload = function() {

        ctx.drawImage(imageObj, 0, 0,width,height); //draw the image first
        beads.colorBeads = translateBeads(beads.colorBeads,height,width); //translate bead coordinates to fit new canvas
        beads.waterBeads = translateBeads(beads.waterBeads,height,width);

        beads.colorBeads.forEach(function(bead){
            drawBead(bead,ctx);
        });
        beads.waterBeads.forEach(function(bead){
            drawBead(bead,ctx);
        });
    };

    $("#colorBeadOutline").change(function(){
        redraw(ctx);
    });
    $("#waterBeadOutline").change(function(){
        redraw(ctx);
    });

    $("#mapCanvas").mousemove(function (e) {
        var rect = canvas.getBoundingClientRect(), //get real coordinates of hover on canvas
            x = e.clientX - rect.left,
            y = e.clientY - rect.top;
        handleHover(x,y,ctx);
    });
});
