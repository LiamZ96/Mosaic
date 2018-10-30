'use-strict'
$(document).ready(function() {
	let buttonA = $('#buttonA'),
		linkA = $('#linkA'),
		buttonB = $('#buttonb'),
		linkB = $('#linkA'),
		overlay = $('#overlay');

	$('.pannable-image').ImageViewer();
	overlay.addClass('d-none');

	buttonA.click(function(e) {
		linkA.click();
	});

	buttonB.click(function(e) {

	});
});