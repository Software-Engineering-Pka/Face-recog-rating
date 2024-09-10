$(document).ready(function() {
    const $video = $('#video-webcam');
    const $canvas = $('canvas');
    const $videoContainer = $('#video-container');
    const $imageData = $('#imageData');
    const $result = $('#result');
    let stream = null;  

    async function streamWebcam() {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        $video[0].srcObject = stream;
    }

    $('#take_photo').click(async function() {
        await streamWebcam(); 
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
            },
            error: function(xhr, status, error) {
                console.error("An error occurred:", error);
            }
        });
    });

    $('#select_picture').change(function() {
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
});
