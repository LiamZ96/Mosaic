'use-strict';
$(window).bind("load", function(){
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