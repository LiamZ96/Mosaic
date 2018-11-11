
/*
    a function to translate a x/y value into a new height/width of a canvas.
    @param coord - the coordinate to translate into a new range. 
    @param oldRange - old height/width.
    @param newRange - new height/width.
*/
var translateCoord = function(coord,oldRange,newRange){
    return ((coord*newRange) / oldRange);
};

$(window).ready(function(){
    const canvas = document.getElementById('mapCanvas'),
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
            bead = bead[2];
            var x = translateCoord(bead[0],imageObj.width,width),
                y = translateCoord(bead[1],imageObj.height,height),
                radius = bead[2]/4;
            ctx.beginPath();
            ctx.arc(x,y,radius,0,2*Math.PI);
            ctx.strokeStyle="red";
            ctx.lineWidth=5;
            ctx.stroke();
        });
    };
});
