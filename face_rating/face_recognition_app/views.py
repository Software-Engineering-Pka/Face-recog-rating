from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
import cv2
import os
from face_recognition_app.face_recog_model import face_recog_model
from account.models import AccountModel

cap = None
sfr = None
recognition_status = {"status": "not_recognized"}

def open_camera():
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)

def close_camera():
    global cap
    if cap and cap.isOpened():
        cap.release()
        cap = None
def stop_webcam(request):
    close_camera()
    return redirect("face_rating_app:face_rating")


def generate_frames(request):
    global cap, sfr
    open_camera()
    sfr = face_recog_model()
    
    sfr.encoding_faces()
        
    while True:
        try:
            success, frame = cap.read()
            if not success:
                break
            face_locations, face_names = sfr.comparing_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
                
                if name != "Unknown":
                    try:
                        account = AccountModel.objects.get(username=name)
                        login(request, account)
              
                    except AccountModel.DoesNotExist:
                        continue 
                
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error in frame processing: {e}")
            break
    
    close_camera()

def video_feed(request):
    return StreamingHttpResponse(generate_frames(request), content_type='multipart/x-mixed-replace; boundary=frame')

def face_recognition_view(request):
    return render(request, 'face_recognition_app/face_recognition.html')
