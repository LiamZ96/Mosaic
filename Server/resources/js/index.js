'use-strict'
$(document).ready(function() {
    let submit = $('#submit'),
        imageForm = $('#image-form'),
        cancelImages = $('#cancel-images'),
        imageUpload = $('#image-upload'),
        slideHolder = $('#slide-holder'),
        alertContainer = $('#alert-container'),
        overlay = $('#overlay'),
        formatTimeout,
        postTimeout;
    
    imageUpload.change(function() {
        let invalidFiles;

        cancelImages.click();

        invalidFiles = Array.from(this.files).filter(function(file) {
            return !(file.name.endsWith('.jpg') || file.name.endsWith('.jpeg'));
        });
    
        if (this.files.length > 0 && invalidFiles.length === 0) {
            if (this.files.length > 1) {
                $('.carousel-control-prev').removeClass('d-none');
                $('.carousel-control-next').removeClass('d-none');
            }
    
            cancelImages.prop('disabled', false);
            submit.prop('disabled', false);
            $('#image-label').text(this.files.length + ' images selected');
    
            $.each(this.files, function(idx, file) {
                let reader = new FileReader();
    
                reader.onload = function(e) {
                    let carouselItem = $('<div class="carousel-item"></div>'),
                        image = $('<img class="d-block w-100"/>')
                            .attr({
                                src: e.target.result,
                                alt: 'Slide ' + slideHolder.children.length
                            }),
                        caption = $('<div class="carousel-caption d-none d-md-block"></div>'),
                        captionText = $('<span class="caption-text"></span>').text(e.target.fileName);
                            
                    if (idx === 0) {
                        carouselItem.addClass('active');
                        $('#placeholder').parent().remove()
                    }
                    
                    caption.append(captionText);
                    carouselItem.append(image);
                    carouselItem.append(caption);
                    slideHolder.append(carouselItem);
                }
    
                reader.fileName = file.name;
                reader.readAsDataURL(file);
            });
        }
        else if (invalidFiles.length > 0) {
            let alert = formatTimeout ? $('#img-alert') : $('<div id="img-alert" class="alert alert-danger my-3" role="alert"><strong>Error</strong> Only files of format .jpg and .jpeg are allowed</div>');

            this.value = null;

            if (formatTimeout) {
                clearTimeout(formatTimeout);
            }
            else {
                alertContainer.prepend(alert);
            }

            window.scrollTo(0, 0);

            formatTimeout = setTimeout(function() {
                alert.remove();
                formatTimeout = null;
            }, 15000);
        }
    });
    
    cancelImages.click(function() {
        let placeholder = $('<div class="carousel-item active"><img id="placeholder" class="d-block w-100" src="/resources/imgs/no-slides.jpg" alt="No Slides"></div>');
    
        cancelImages.prop('disabled', true);
        submit.prop('disabled', true);
        $('.carousel-control-prev').addClass('d-none');
        $('.carousel-control-next').addClass('d-none');
        $('#image-label').text('Choose images');
    
        while (slideHolder.children().length !== 0) {
            slideHolder.children()[0].remove();
        }
    
        placeholder.addClass('active');
        slideHolder.append(placeholder);
    });
    
    submit.click(function() {
        let data = new FormData(imageForm[0]);

        overlay.removeClass("d-none");

        $.ajax({
            method: 'POST',
            url: '/uploadImages',
            enctype: "multipart/form-data",
            data: data,
            cache: false,
            contentType: false,
            processData: false
        })
        .done(function(e) {
            if (e.status === 0) {
                // TODO: Add in location of next view
                window.location.replace("nextView");
            }
            else {
                postFail();
            }
        })
        .fail(postFail)
    });

    function postFail() {
        let alert = postTimeout ? $('#post-alert') : $('<div id="post-alert" class="alert alert-danger my-3" role="alert"><strong>Error</strong> An error occured while uploading images, please try again later.</div>');

<<<<<<< HEAD
        overlay.addClass("d-none");

        if (postTimeout) {
            clearTimeout(postTimeout);
        }
        else {
            alertContainer.prepend(alert);
        }

        window.scrollTo(0, 0);

        postTimeout = setTimeout(function() {
            alert.remove();
            postTimeout = null;
        }, 15000);
    }
=======
dropdownItem.on("click", function (e) {
    e.preventDefault();
    var magLevel = $(this).html();
    magLevelButton.text("Mag Level: " + magLevel);
    $("#magLevelInput").val(magLevel);
});


submit.click(function() {
    imageForm.submit();
>>>>>>> develop
});