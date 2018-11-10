$(window).ready(function(){
    const canvas = document.getElementById('mapCanvas'),
        canvasWrapper = $("#canvasWrapper"),
        ctx = canvas.getContext('2d'),
        imageObj = new Image(),
        height = canvasWrapper.height() * 2,
        width = canvasWrapper.width();

    imageObj.src = mapLocation;
    imageObj.onload = function() {
        ctx.canvas.width = width;
        ctx.canvas.height = height;

      ctx.drawImage(imageObj, 0, 0,width,height);
    };
});
