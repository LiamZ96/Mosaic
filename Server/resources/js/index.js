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

//Requirements in this file: 3.2.1, 3.4.1.1
//Authors: Jacob Wakefield, Noah Zeilmann, McKenna Gates

'use-strict'
$(document).ready(function() {
    let submit = $('#submit'),
        imageForm = $('#image-form'),
        videoForm = $('#video-form'),
        cancelImages = $('#cancel-images'),
        cancelVideo = $('#cancel-video'),
        imageUpload = $('#image-upload'),
        videoUpload = $('#video-upload'),
        videoSource = $('#video-src'),
        slideHolder = $('#slide-holder'),
        videoHolder = $('#video-holder'),
        alertContainer = $('#alert-container'),
        overlay = $('#overlay'),
        timeoutMgr = {
            imgFormatTimeout: null,
            videoFormatTimeout: null,
            postTimeout: null,
        }
        prevSrc = null;
    
    imageUpload.change(function(e) {
        let invalidFiles;

        cancelImagePreview();
        cancelVideo.click();

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
                        $('#img-placeholder').parent().remove()
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
            createAlert('img-alert', 'Only image files of format .jpg and .jpeg are allowed', 'imgFormatTimeout');
            this.value = null;
        }
    });

    videoUpload.change(function(e) {
        cancelImages.click();

        if (this.files[0].name.endsWith('.avi')) {
            videoSource[0].src = URL.createObjectURL(this.files[0]);
            videoSource.parent()[0].load();
            videoSource.parent().removeClass('d-none');
            videoUpload.parent().parent().addClass('selected-vid');

            if ($('#video-placeholder')) {
                $('#video-placeholder').remove();
                prevSrc = videoSource[0].src;
            }
            else {
                URL.revokeObjectURL(prevSrc);
            }
            
            $('#video-label').text(this.files[0].name);

            cancelVideo.prop('disabled', false);
            submit.prop('disabled', false);
        }
        else {
            createAlert('video-alert', 'Only video files of format .avi are allowed', 'videoFormatTimeout');
            this.value = null;
        }
    });

    cancelVideo.click(function() {
        if (videoUpload.val() != null && videoUpload.val() !== '') {
            let placeholder = $('<img id="video-placeholder" class="d-block w-100" src="/resources/imgs/no-video.jpg" alt="No Video"/>');
        
            cancelVideo.prop('disabled', true);
            submit.prop('disabled', true);
            $('#video-label').text('Choose video');
        
            URL.revokeObjectURL(videoSource[0].src);
            videoSource[0].src = '';
            videoSource.parent()[0].load();
            videoSource.parent().addClass('d-none');
            videoUpload.parent().parent().removeClass('selected-vid');
            videoUpload.val(null);

            videoHolder.prepend(placeholder);
        }
    });
    
    cancelImages.click(function() {
        cancelImagePreview();
        imageUpload.val(null);
    });
    
    submit.click(function() {
        let data = imageUpload.val() != null && imageUpload.val() !== '' ? new FormData(imageForm[0]) : new FormData(videoForm[0]);

        overlay.removeClass('d-none');

        $.ajax({
            method: 'POST',
            url: imageUpload.val() != null && imageUpload.val() !== '' ? '/uploadImages' : '/uploadVideo',
            enctype: 'multipart/form-data',
            data: data,
            cache: false,
            contentType: false,
            processData: false
        })
        .done(function(e) {
            if (e.status === 0) {
                window.location.href = 'getStitchedImage'+e.location;
            }
            else {
                postFail();
            }
        })
        .fail(postFail)
    });

    function createAlert(id, msg, mgrId) {
        let alert = timeoutMgr[mgrId] ? $('#' + id) : $('<div id=' + id + ' class="alert alert-danger my-3" role="alert"><strong>Error</strong> ' + msg + '</div>');

        if (timeoutMgr[mgrId]) {
            clearTimeout(timeoutMgr[mgrId]);
        }
        else {
            alertContainer.prepend(alert);
        }

        window.scrollTo(0, 0);

        timeoutMgr[mgrId] = setTimeout(function() {
            alert.remove();
            timeoutMgr[mgrId] = null;
        }, 15000);
    }

    function cancelImagePreview() {
        let placeholder = $('<div class="carousel-item active"><img id="img-placeholder" class="d-block w-100" src="/resources/imgs/no-slides.jpg" alt="No Slides"></div>');
    
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
    }

    function postFail(e) {
        overlay.addClass('d-none');
        createAlert('post-alert', 'An error occured while uploading your files, please try again later.', 'postTimeout');
    }
});