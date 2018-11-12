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
		colorAry.push(fullColorHex(Math.round(circle[0][0]), Math.round(circle[0][1]), Math.round(circle[0][2])));
		i++;
	});


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
});