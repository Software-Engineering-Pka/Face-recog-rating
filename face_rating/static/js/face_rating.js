$(document).ready(function() {
    const $video = $('#video-webcam');
    const $canvas = $('canvas');
    const $videoContainer = $('#video-container2');
    const $imageData = $('#imageData');
    const $result = $('#result');
    const $face_rating_btn = $("#face_rating_btn")
    let stream = null;  
    let $overlay = $(".overlay")
    let $rating_session = $("#rating_section")
    async function streamWebcam() {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        $video[0].srcObject = stream;
    }

    $('#take_photo').click(async function() {
        $(".container-content").css({
            display:"none"
        })
        await streamWebcam(); 
        $videoContainer.css({
            display:"block"
        })
        $videoContainer.show();
    });

    $('#btn').click(function(event) {
        event.preventDefault(); 

        const ctx = $canvas[0].getContext("2d");
        ctx.drawImage($video[0], 0, 0, $canvas[0].width, $canvas[0].height);
        const imageData = $canvas[0].toDataURL('image/png');
        $imageData.val(imageData);
        console.log($imageData.val());

        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        $videoContainer.hide();

        $.ajax({
            type: 'POST',
            url: window.location.href, 
            data: {
                'imageData': imageData,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                $result.text(response.result);
                $('#editedImage').attr('src', 'data:image/jpeg;base64,' + response.edited_image);
                $('#editedImage').css({
                    display:"block"
                })
                console.log("Hello",response.edited_image)
                $rating_session.css({
                    display:"block"
                })
            },
            error: function(xhr, status, error) {
                console.error("An error occurred:", error);
            }
        });
    });

    $("#select_photo").off("click").on("click", function() {
        $('#select_picture').click();
    });
    
    $('#select_picture').on("change",function() {
            const file = this.files[0];
            if (file) {
                const formData = new FormData();
                formData.append('image', file);
                $.ajax({
                    url: '/upload/',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    success: function(response) {
                        $result.text(response.result);
                        $('#editedImage').attr('src', 'data:image/jpeg;base64,' + response.edited_image);
                        $('#editedImage').css({
                            display:"block"
                        })
                        $overlay.css({
                            display:"none"
                        })
                        $rating_session.css({
                            display:"block"
                        })
                        console.log('Upload successful:', response);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error:', error);
                    }
                });
            }
    });
    
    

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(cookie => {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                }
            });
        }
        return cookieValue;
    }
    $face_rating_btn.on("click",function () {
        $(".action-buttons").css({
            display:"block"
        })
        $(".test-options").css({
            display:"none"
        })
    })
});
