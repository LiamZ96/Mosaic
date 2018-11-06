'use strict';

$(window).ready(function(){

	let rgbToHex = function (rgb) { 
		var hex = Number(rgb).toString(16);
		if (hex.length < 2) {
			 hex = "0" + hex;
		}
		return hex;
	  };

	  let fullColorHex = function(r,g,b) {   
		var red = rgbToHex(r);
		var green = rgbToHex(g);
		var blue = rgbToHex(b);
		return '#' + red+green+blue;
	  };


	console.log(circles);
	let colorAry = [];

	
	//CanvasJS.addColorSet("red", ['#8F1500']);
	CanvasJS.addColorSet("green", ['#007F00']);
	CanvasJS.addColorSet("blue", ['#1034A6']);

	let red = [],
		green = [],
		blue = [],
		i = 0;		
		
	for (var key in circles) {
		var redBeadData = {},
			greenBeadData = {},
			blueBeadData = {};
		redBeadData.label = i;
		greenBeadData.label = i;
		blueBeadData.label = i;
		redBeadData.y = circles[i][0][0];
		greenBeadData.y = circles[i][0][1];
		blueBeadData.y = circles[i][0][2];
		red.push(redBeadData);
		green.push(greenBeadData);
		blue.push(blueBeadData);
		colorAry.push(fullColorHex(Math.round(circles[i][0][0]), Math.round(circles[i][0][1]), Math.round(circles[i][0][2])));
		i++;
	};

	CanvasJS.addColorSet("red", colorAry);
	console.log(colorAry);

	var redChart = {
		colorSet: "red",
		title: {
			text: "R-Values"              
		},
		data: [              
		{
			// Change type to "doughnut", "line", "splineArea", etc.
			type: "column",
			dataPoints: red
		}
		]
	};
	var greenChart = {
		colorSet: "red",
		title: {
			text: "G-Values"              
		},
		data: [              
		{
			// Change type to "doughnut", "line", "splineArea", etc.
			type: "column",
			dataPoints: green
		}
		]
	};
	var blueChart = {
		colorSet: "red",
		title: {
			text: "B-Values"              
		},
		data: [              
		{
			// Change type to "doughnut", "line", "splineArea", etc.
			type: "column",
			dataPoints: blue
		}
		]
	};

	$("#redChart").CanvasJSChart(redChart);
	$("#greenChart").CanvasJSChart(greenChart);
	$("#blueChart").CanvasJSChart(blueChart);


	var addImages = function(){
		
		let address = $(location).attr('href'),
			parts = address.split("/"),
			last_part = parts[parts.length-1],
			r = $.Deferred(),
			imageLocation = "/resources/uploads/" + last_part + "/results/";
		for(let i = 0; i < ImageDiv.dataset.numimages-1;i++){
			$("#ImageDiv").append( "<img src='"+ imageLocation + "result_image"+ i +".jpg" +"' id=image"+ i +">");
		}
		return r;
	};
	var shrinkImages = function(){
		for(let j = 0; j < ImageDiv.dataset.numimages-1;j++){
			let imageVar = "#image" + j.toString();
			if ($(imageVar).width() > 1200){
				let width = $("#image" + j.toString()).width(),
					height = $("#image" + j.toString()).height();
				width *= .5;
				height *=.5;
				$(imageVar).width(width);
				$(imageVar).height(height);
			}
		}
	};


	addImages().done(shrinkImages());
});