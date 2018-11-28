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
	let j = 0;


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
		let hex = Number(rgb).toString(16);
		if (hex.length < 2) {
			 hex = "0" + hex;
		}
		return hex;
	  };

	  let fullColorHex = function(r,g,b) {   
		let red = rgbToHex(r);
		let green = rgbToHex(g);
		let blue = rgbToHex(b);
		return '#' + red+green+blue;
	  };

	let red = [],
		green = [],
		blue = [],
		i;		

	beads.colorBeads.forEach(function(circle){
		red.push(circle[0][0]);
		green.push(circle[0][1]);
		blue.push(circle[0][2]);
		//colorAry.push(fullColorHex(Math.round(circle[0][0]), Math.round(circle[0][1]), Math.round(circle[0][2])));
		//console.log(getHue(Math.round(circle[0][0]), Math.round(circle[0][1]), Math.round(circle[0][2])));
		i++;
	});


	// CanvasJS.addColorSet("red", colorAry);
	// console.log(colorAry);

	let redChart = {
		colorSet: "red",
		title: {
			text: "R-Values"              
		},
		data: [              
		{
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
			type: "column",
			dataPoints: blue
		}
		]
	};

	//New Histogram
	let trace1 = {
		x: red,
		name: 'red',
		autobinx: false, 
		histnorm: "count", 
		marker: {
			color: "rgba(255, 100, 102, 0.7)", 
			line: {
			color:  "rgba(255, 100, 102, 1)", 
			width: 1
			}
		},  
		opacity: 0.5, 
		type: "histogram", 
		xbins: {
			end: 255, 
			size: 5, 
			start: 0
		}
	};
	let trace2 = {
		x: green,
		autobinx: false, 
		marker: {
				color: "rgba(100, 200, 102, 0.7)",
				line: {
					color:  "rgba(100, 200, 102, 1)", 
					width: 1
			} 
			}, 
		name: "green", 
		opacity: 0.75, 
		type: "histogram", 
		xbins: { 
			end: 255, 
			size: 5, 
			start: 0

		}
	};
	let trace3 = {
		x: blue,
		autobinx: false, 
		marker: {
				color: "#b1cfeb",
				line: {
					color:  "#447bdc", 
					width: 1
			} 
			}, 
		name: "blue", 
		opacity: 0.75, 
		type: "histogram", 
		xbins: { 
			end: 255, 
			size: 5, 
			start: 0

		}
	};
	let data = [trace1, trace2, trace3];
	let red_layout = {
		bargap: 0.05, 
		bargroupgap: 0.2, 
		barmode: "overlay", 
		title: "Red Values", 
		xaxis: {title: "R Value"}, 
		yaxis: {title: "Count"}
	};
	let green_layout = {
		bargap: 0.05, 
		bargroupgap: 0.2, 
		barmode: "overlay", 
		title: "G Values", 
		xaxis: {title: "G Value"}, 
		yaxis: {title: "Count"}
	};
	let blue_layout = {
		bargap: 0.05, 
		bargroupgap: 0.2, 
		barmode: "overlay", 
		title: "B Values", 
		xaxis: {title: "B Value"}, 
		yaxis: {title: "Count"}
	};
	Plotly.newPlot('redChart', [trace1], red_layout);
	Plotly.newPlot('greenChart', [trace2], green_layout);
	Plotly.newPlot('blueChart', [trace3], blue_layout);
});