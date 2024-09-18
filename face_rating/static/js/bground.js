function diChuyenVaLacLuAnh() {
    const image = document.querySelector('.logo img'); // Chọn hình ảnh trong class .logo
    let gocLac = 0; // Biến dùng để lắc lư
    let viTriX = 0; // Biến dùng để di chuyển theo trục X
    let direction = 1; // Hướng lắc và di chuyển
    let speed = 1; // Tốc độ di chuyển và lắc lư

    setInterval(function() {
        // Lắc lư từ -3 đến 3 độ
        gocLac += direction * 1;
        if (gocLac > 3 || gocLac < -3) {
            direction *= -1; // Đổi hướng khi lắc đạt biên độ tối đa
        }

        // Di chuyển từ -10px đến 10px theo chiều ngang
        viTriX += direction * speed;
        if (viTriX > 10 || viTriX < -10) {
            speed *= -1; // Đổi hướng di chuyển khi đạt giới hạn
        }

        // Áp dụng cả hai hiệu ứng lắc lư và di chuyển
        image.style.transform = `translateX(${viTriX}px) rotate(${gocLac}deg)`;
    }, 150); // Điều chỉnh tốc độ
}

// Gọi hàm diChuyenVaLacLuAnh ngay khi trang tải xong
window.onload = function() {
    diChuyenVaLacLuAnh();
};
