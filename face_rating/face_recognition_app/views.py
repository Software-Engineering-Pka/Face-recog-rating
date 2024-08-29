from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
import cv2
import os
from face_recognition_app.face_recog_model import face_recog_model

# Đối tượng camera dùng chung và mô hình nhận diện khuôn mặt
cap = None
sfr = None

def open_camera():
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)

def close_camera():
    global cap
    if cap and cap.isOpened():
        cap.release()
        cap = None

def generate_frames():
    global cap, sfr
    open_camera()  # Mở camera dùng chung
    sfr = face_recog_model()
    sfr.encoding_faces(os.path.join(settings.MEDIA_ROOT, 'images'))
        
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Xử lý frame để nhận diện khuôn mặt
            face_locations, face_names = sfr.comparing_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

            # Mã hóa frame thành JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    close_camera()  # Đóng camera khi kết thúc

def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def face_recognition_view(request):
    global sfr
    if request.method == 'POST':
        # Khởi tạo mô hình nhận diện khuôn mặt
        
        # Capture một khung hình từ webcam
        open_camera()
        ret, frame = cap.read()
        close_camera()

        if not ret:
            return JsonResponse({'error': 'Unable to capture video frame'}, status=500)

        # Thực hiện nhận diện khuôn mặt trên khung hình
        # face_locations, face_names = sfr.comparing_faces(frame)
        # results = [{'name': name, 'location': list(face_loc)} for face_loc, name in zip(face_locations, face_names)]

        # return JsonResponse({'faces': results})

    return render(request, 'face_recognition_app/upload.html')
