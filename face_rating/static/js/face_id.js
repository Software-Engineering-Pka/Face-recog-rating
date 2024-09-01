const btnChup = document.getElementById("btn")
const video = document.getElementById("video-webcam")
const canvas = document.querySelector('canvas')

async function streamWebcam() {
    const stream = await navigator.mediaDevices.getUserMedia({
        video: true
    })
    video.srcObject = stream
}
streamWebcam()
btnChup.addEventListener("click", async () => {
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Chuyển đổi canvas thành base64
    const imageData = canvas.toDataURL('image/png');
    
    // Cập nhật giá trị của trường input
    $("#imageData").val(imageData);
    
    console.log($("#imageData").val());
    
    // Gửi dữ liệu ảnh tới server
});