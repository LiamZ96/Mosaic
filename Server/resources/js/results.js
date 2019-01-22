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

//Author: Luke Johnson

'use strict';

$(window).ready(function(){

	let beadTableDiv = document.getElementById('resultsDiv'),
		table = document.createElement('table'),
		tableHeader = document.createElement('thead'),
		tableHeaderRow = document.createElement('tr'),
		beadNumberHeader = document.createElement('th'),
		rValueHeader = document.createElement('th'),
		gValueHeader = document.createElement('th'),
		bValueHeader = document.createElement('th'),
		j = 0;

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


	let getColorName = function(red, green, blue) {
		let hue = getHue(red, green, blue);	
		if (hue < 30)   
			return "red";
		if (hue < 90)   
			return "yellow";
		if (hue < 150)  
			return "green";
		if (hue < 210)
			return "cyan";
		if (hue < 270)
			return "blue";
		if (hue < 330)  
			return "magenta";
		return "red";
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
	
	let rgbToHsl = function(r,g,b) { 
		return  {	
			hue: getHue(r, g, b),
			saturation: getSaturation(r, g, b),
			luminance: getLuminance(r, g, b) 
		};
	};

	let getRatio = (value) => {
		return (value/255).toFixed(4);
    }

	let getHue = (r, g, b) => {
		let min, max, hue = 0;
		r = getRatio(r);
		g = getRatio(g);
		b = getRatio(b);
		min = Math.min(r, g, b);
		max = Math.max(r, g, b);
	
		if (min == max) return hue;

		if (max == r) 
			hue = (g - b) / (max - min);	
		else if (max == g) 
			hue = 2 + (b - r) / (max - min);	
		else
			hue = 4 + (r - g) / (max - min);
	
		hue = Math.round(hue * 60);
		if (hue < 0) hue = hue + 360;
		return hue.toFixed(2);
	}

	let getSaturation = (r, g, b) => {
		let min, max, saturation, luminance = getLuminance(r, g, b) / 100;
		r = getRatio(r);
		g = getRatio(g);
		b = getRatio(b);
		min = Math.min(r, g, b);
		max = Math.max(r, g, b);
			
		if(luminance < 1)
			saturation = (max - min) / (1 - Math.abs(2 * luminance - 1))
		else if(luminance == 1)
			saturation = 0;
		
		return (saturation * 100).toFixed(2);
	}

	let getLuminance = (r, g, b) => {
		r = getRatio(r);
		g = getRatio(g);
		b = getRatio(b);
		return (((Math.min(r, g, b) + Math.max(r, g, b))/2) * 100).toFixed(2);
	}

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

	let red = [], green = [], blue = [], hue = [], saturation = [], luminance = [],
	i = 0, nameAry = [],redCount = 0, yellowCount = 0, greenCount = 0, cyanCount = 0,
	blueCount = 0, magentaCount = 0, countedString = `There were `;	

	let countColor = (color) => {
		if(color === 'red')
			redCount++;
		else if(color === 'yellow')
			yellowCount++;
		else if(color === 'green')
			greenCount++;
		else if(color === 'cyan')
			cyanCount++;
		else if(color === 'blue')
			blueCount++;
		else if(color === 'magenta')
			magentaCount++;
	}

	beads.colorBeads.forEach(function(circle){
		let r = circle[0][0], g = circle[0][1], b = circle[0][2];
		red.push(r);
		green.push(g);
		blue.push(b);
		hue.push(Number(getHue(r, g, b)));
		saturation.push(Number(getSaturation(r, g, b)));
		luminance.push(Number(getLuminance(r, g, b)));
		nameAry.push((i+1).toString());
		i++;
		countColor(getColorName(Math.round(r), Math.round(g), Math.round(b)));	
	});
	console.log(nameAry)
	if(yellowCount>0)
		countedString += `${yellowCount} yellow beads, `;
	if(redCount>0)
		countedString += `${redCount} red beads, `;
	if(greenCount>0)
		countedString += `${greenCount} green beads, `;
	if(cyanCount>0)
		countedString += `${cyanCount} cyan beads, `;
	if(blueCount>0)
		countedString += `${blueCount} blue beads, `;
	if(magentaCount>0)
		countedString += `${magentaCount} magenta beads `;
	countedString += `${beads.colorBeads.length} total beads, and ${beads.waterBeads.length} water beads detected.`;

	document.getElementById('CountDiv').innerText = countedString;


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
	//New Scatter Plots
	let r_g = {
		x: green,
		y: red,
		mode: 'markers',
		type: 'scatter',
		name: '',
		text: nameAry,
		marker: { size: 12 }
	  };
	  let r_g_layout = {
		xaxis: {
          range: [ 0, 265 ],
          title: "Green Value"
          
		},
		yaxis: {
            range: [ 0, 265 ],
            title: "Red Value"
		},
		title:'Red V Green'
	  };
	  let r_b = {
		x: blue,
		y: red,
		mode: 'markers',
		type: 'scatter',
		name: '',
		text: nameAry,
		marker: { size: 12 }
	  };
	  let r_b_layout = {
		xaxis: {
            range: [ 0, 265 ],
            title: "Blue Value"
		},
		yaxis: {
            range: [ 0, 265 ],
            title: "Red Value"
		},
		title:'Red V Blue'
	  };
	  let g_b = {
		x: blue,
		y: green,
		mode: 'markers',
		type: 'scatter',
		name: '',
		text: nameAry,
		marker: { size: 12 }
	  };
	  let g_b_layout = {
		xaxis: {
            range: [ 0, 265 ],
            title: "Blue Value"
		},
		yaxis: {
            range: [ 0, 265 ],
            title: "Green Value"
		},
		title:'Green V Blue'
	  };
	  let sat_hue = {
		x: hue,
		y: saturation,
		mode: 'markers',
		type: 'scatter',
		name: 'Saturation V Hue',
		text: nameAry,
		marker: { size: 12 }
	  };
	  let sat_hue_layout = {
		xaxis: {
          range: [ 0, 360 ],
          title: "Hue Value (in degrees)"
		},
		yaxis: {
          range: [ 0, 110 ],
          title: "% Saturation"
		},
		title:'Saturation V Hue'
	  };
	  let lum_hue = {
		x: hue,
		y: luminance,
		mode: 'markers',
		type: 'scatter',
		name: 'Luminance V Hue',
		text: nameAry,
		marker: { size: 12 }
	  };
	  let lum_hue_layout = {
		xaxis: {
		  range: [ 0, 360 ],
          title: "Hue Value (in degrees)"
		},
		yaxis: {
		  range: [ 0, 110 ],
          title: "% Luminance"
		},
		title:'Luminance V Hue'
	  };
	  let lum_sat = {
		x: saturation,
		y: luminance,
		mode: 'markers',
		type: 'scatter',
		name: 'Luminance V Saturation',
		text: nameAry,
		marker: { size: 12 }
	  };
	  let lum_sat_layout = {
		xaxis: {
		  range: [ 0, 110 ],
          title: "% Saturation"
		},
		yaxis: {
		  range: [ 0, 110 ],
          title: "% Luminance"
		},
		title:'Luminance V Saturation'
	  };

	//New Histograms
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
	let combined_layout = {
		bargap: 0.05, 
		bargroupgap: 0.2, 
		barmode: "overlay", 
		title: "Combined Graph", 
		xaxis: {title: "Value"}, 
		yaxis: {title: "Count"}
	};
	Plotly.newPlot('combinedChart', [trace1, trace2, trace3], combined_layout);
	Plotly.newPlot('redChart', [trace1], red_layout);
	Plotly.newPlot('greenChart', [trace2], green_layout);
	Plotly.newPlot('blueChart', [trace3], blue_layout);

	Plotly.newPlot('r_g', [r_g], r_g_layout);
	Plotly.newPlot('r_b', [r_b], r_b_layout);
	Plotly.newPlot('g_b', [g_b], g_b_layout);
	Plotly.newPlot('sat_hue', [sat_hue], sat_hue_layout);
	Plotly.newPlot('lum_hue', [lum_hue], lum_hue_layout);
	Plotly.newPlot('lum_sat', [lum_sat], lum_sat_layout);

	document.getElementById('btn').addEventListener('click', () => {
		event.preventDefault();
		let bucketSize = document.getElementById('bucketSize').value;
		trace1.xbins.size = bucketSize;
		trace2.xbins.size = bucketSize;
		trace3.xbins.size = bucketSize;
		
		Plotly.newPlot('combinedChart', [trace1, trace2, trace3], combined_layout);
		Plotly.newPlot('redChart', [trace1], red_layout);
		Plotly.newPlot('greenChart', [trace2], green_layout);
		Plotly.newPlot('blueChart', [trace3], blue_layout);
	});

});

