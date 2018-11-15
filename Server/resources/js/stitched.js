'use-strict'
$(document).ready(function() {
	let buttonA = $('#buttonA'),
		buttonB = $('#buttonb'),
		overlay = $('#overlay'),
		magSelect = $("#mag-select");


	$('.pannable-image').ImageViewer();
	overlay.addClass('d-none');

	buttonA.click(function(e) {
		window.location.replace(LOCATION_A+"?magLevel="+magSelect.val());
	});

	buttonB.click(function(e) {
		window.location.replace(LOCATION_B+"?magLevel="+magSelect.val());
	});
});