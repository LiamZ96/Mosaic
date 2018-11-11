var clearToolTipCallback = undefined; //callback to called when no bead is being hovered over

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
    @param bead - the bead to be drawn. 
    @param imageObj - the map image.
    @param ctx - the context of the canvas.
    @param width - the width of the canvas. 
    @param height - the height of the canvas.
*/
var drawBead = function(bead,imageObj,ctx,width,height) {
    bead = bead[2];
    var x = translateCoord(bead[0],imageObj.width,width),
        y = translateCoord(bead[1],imageObj.height,height),
        radius = bead[2]/4; //TODO: translate this radius like the x,y
    ctx.beginPath();
    ctx.arc(x,y,radius,0,2*Math.PI);
    ctx.strokeStyle="red";
    ctx.lineWidth=5;
    ctx.stroke();

    //set the new values in the bead array
    bead[0] = x;
    bead[1] = y; 
    bead[2] = radius; 
};

// x,y is the point to test
// cx, cy is circle center, and radius is circle radius
var pointInCircle = function(x, y, cx, cy, radius) {
    return Math.sqrt((x-cx)*(x-cx) + (y-cy)*(y-cy)) < radius;
}

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
        ctx.fillStyle = "white";
        ctx.fillRect(rectX,rectY, rectWidth, rectHeight);
        // draw font in red
        ctx.fillStyle = "black";
        ctx.font = "10pt sans-serif";
        var text = "RGB: ("+toolTipBead[0][0]+", "+toolTipBead[0][1]+", "+toolTipBead[0][2] + ")    isWater: "+toolTipBead[1];
        ctx.fillText(text,rectX+10,rectY+(rectHeight/2),rectX+rectWidth);
        clearToolTipCallback = function(){
            ctx.clearRect(rectX,rectY,rectWidth,rectHeight);
        };
    }else{
        //clearToolTipCallback ? clearToolTipCallback() : undefined;
    }
};

$(window).ready(function() {
    var canvas = document.getElementById('mapCanvas'),
        canvasWrapper = $("#canvasWrapper"),
        ctx = canvas.getContext('2d'),
        imageObj = new Image(),
        height = canvasWrapper.height() * 2, //set the height based on the save of the canvas wrapper * 2
        width = canvasWrapper.width(); //set the width based on the save of the canvas wrapper
        
    imageObj.src = mapLocation;
    ctx.canvas.width = width;
    ctx.canvas.height = height;
    
    imageObj.onload = function() {

        ctx.drawImage(imageObj, 0, 0,width,height); //draw the image first
        beads.colorBeads.forEach(function(bead){
            drawBead(bead,imageObj,ctx,width,height);
        });
        beads.waterBeads.forEach(function(bead){
            drawBead(bead,imageObj,ctx,width,height);
        });
    };

    $("#mapCanvas").mousemove(function (e) {
        handleHover(e.clientX,e.clientY,ctx);
    });
});
