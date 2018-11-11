
var translateCoord = function(coord,oldRange,newRange){
    return ((coord*newRange) / oldRange);
};

$(window).ready(function(){
    const canvas = document.getElementById('mapCanvas'),
        canvasWrapper = $("#canvasWrapper"),
        ctx = canvas.getContext('2d'),
        imageObj = new Image(),
        height = canvasWrapper.height() * 2,
        width = canvasWrapper.width();
        
    imageObj.src = mapLocation;
    ctx.canvas.width = width;
    ctx.canvas.height = height;

    imageObj.onload = function() {
        ctx.drawImage(imageObj, 0, 0,width,height);
        beads.colorBeads.forEach(function(bead){
            bead = bead[2];
            var x = translateCoord(bead[0],imageObj.width,width),
                y = translateCoord(bead[1],imageObj.height,height);
            ctx.beginPath();
            ctx.arc(x,y,bead[2]/4,0,2*Math.PI);
            ctx.strokeStyle="red";
            ctx.lineWidth=5;
            ctx.stroke();
        });
    };
});
