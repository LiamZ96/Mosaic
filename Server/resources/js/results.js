'use strict';

$(window).ready(function(){

	let beadTableDiv = document.getElementById('resultsDiv'),
		table = document.createElement('table'),
		tableHeader = document.createElement('thead'),
		tableHeaderRow = document.createElement('tr'),
		beadNumberHeader = document.createElement('th'),
		rValueHeader = document.createElement('th'),
		gValueHeader = document.createElement('th'),
		bValueHeader = document.createElement('th');

	table.className = 'table table-sm';
	beadNumberHeader.innerText = '#';
	rValueHeader.innerText = 'R';
	gValueHeader.innerText = 'G';
	bValueHeader.innerText = 'B';	

	beadNumberHeader.setAttribute("scope", "col");
	rValueHeader.setAttribute("scope", "col");
	gValueHeader.setAttribute("scope", "col");
	bValueHeader.setAttribute("scope", "col");	

	tableHeaderRow.appendChild(beadNumberHeader);
	tableHeaderRow.appendChild(rValueHeader);
	tableHeaderRow.appendChild(gValueHeader);
	tableHeaderRow.appendChild(bValueHeader);
	tableHeader.appendChild(tableHeaderRow);
	table.appendChild(tableHeader);


	let getHue = function(red, green, blue) {

		let min = Math.min(Math.min(red, green), blue);
		let max = Math.max(Math.max(red, green), blue);
	
		if (min == max) {
			return 0;
		}
	
		let hue = 0;
		if (max == red) {
			hue = (green - blue) / (max - min);
	
		} else if (max == green) {
			hue = 2 + (blue - red) / (max - min);
	
		} else {
			hue = 4 + (red - green) / (max - min);
		}
	
		hue = Math.round(hue * 60);
		if (hue < 0) hue = hue + 360;
	
		if (hue < 30)   return "Reds";
		if (hue < 90)   return "Yellows";
		if (hue < 150)  return "Greens";
		if (hue < 210)  return "Cyans";
		if (hue < 270)  return "Blues";
		if (hue < 330)  return "Magentas";
		return "Reds";
		//return Math.round(hue);
	}
		
	for (var key in circles) {

	var j = 0;
	beads.colorBeads.forEach(function(circle){

		let newRow = document.createElement('tr'),
			beadNumber = document.createElement('th'),
			bead_r_value = document.createElement('td'),
			bead_g_value = document.createElement('td'),
			bead_b_value = document.createElement('td');
	
			beadNumber.setAttribute("scope", "row");
			beadNumber.innerText = j + 1;
			bead_r_value.innerText = Math.round(circle[0][0]);
			bead_g_value.innerText = Math.round(circle[0][1]);
			bead_b_value.innerText = Math.round(circle[0][2]);
	
			newRow.appendChild(beadNumber);
			newRow.appendChild(bead_r_value);
			newRow.appendChild(bead_g_value);
			newRow.appendChild(bead_b_value);
	
			table.appendChild(newRow);
		j++;
	
	});
	document.getElementsByClassName('graphdiv')[0].replaceChild(table, beadTableDiv);



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

	let colorAry = [];

	
	//CanvasJS.addColorSet("red", ['#8F1500']);
	CanvasJS.addColorSet("green", ['#007F00']);
	CanvasJS.addColorSet("blue", ['#1034A6']);

	let red = [],
		green = [],
		blue = [],
		i;		

	beads.colorBeads.forEach(function(circle){
		var redBeadData = {},
			greenBeadData = {},
			blueBeadData = {};
		redBeadData.label = i;
		greenBeadData.label = i;
		blueBeadData.label = i;
		redBeadData.y = circle[0][0];
		greenBeadData.y = circle[0][1];
		blueBeadData.y = circle[0][2];
		red.push(redBeadData);
		green.push(greenBeadData);
		blue.push(blueBeadData);
		colorAry.push(fullColorHex(Math.round(circles[i][0][0]), Math.round(circles[i][0][1]), Math.round(circles[i][0][2])));
		console.log(getHue(Math.round(circles[i][0][0]), Math.round(circles[i][0][1]), Math.round(circles[i][0][2])));
		i++;
	});


	CanvasJS.addColorSet("red", colorAry);

	let redChart = {
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
	let greenChart = {
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
	let blueChart = {
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

	let addImages = function(){
		
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
	let shrinkImages = function(){
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