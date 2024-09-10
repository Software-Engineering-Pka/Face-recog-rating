from django.shortcuts import render, redirect, HttpResponse
from imutils import face_utils
import dlib
import cv2
from .score_model import ScoreModel
from django.conf import settings
import os
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def home(request):
    return render(request,"face_rating_app/home.html")
def face_rating(request):
    if request.method == "POST":
        try:
            base64_string = request.POST.get("imageData")
            header, base64_data = base64_string.split(';base64,')
            image_data = base64.b64decode(base64_data)
            image = np.array(Image.open(BytesIO(image_data)))
            result = scoring_face(image)
            result=str(result)
            return JsonResponse({"result":result})
        except: 
            print("error")
 
    return render(request,"face_rating_app/face_rating.html")

def scoring_face(image):
    p = os.path.join(settings.MEDIA_ROOT,"algorithm_files","shape_predictor_68_face_landmarks.dat")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(p)
    # Load the image and convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the grayscale image
    rects = detector(gray, 0)

    # Loop over the face detections
    for (i, rect) in enumerate(rects):
        # Get the facial landmarks
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        # Extract the coordinates of the eyes
        left_eye = shape[36:42]  # Points for the left eye
        right_eye = shape[42:48] # Points for the right eye
        face_center_point = (left_eye[0][0] + right_eye[3][0]) // 2

        nose_points = shape[27:35] 
        mouth_points = shape[48:67]
        jawline_points = shape[0:17]
        # Draw the eye contours on the image
        cv2.polylines(image, [left_eye], isClosed=True, color=(255, 0, 0), thickness=1)
        cv2.polylines(image, [right_eye], isClosed=True, color=(255, 0, 0), thickness=1)
        cv2.polylines(image, [nose_points], isClosed=True, color=(255, 255, 0), thickness=1)
        cv2.polylines(image, [mouth_points], isClosed=True, color=(255, 255, 255), thickness=1)
        cv2.polylines(image, [jawline_points], isClosed=False, color=(0, 255, 255), thickness=1)
        # Draw the landmarks for the eyes
        for (x, y) in left_eye:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        for (x, y) in right_eye:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        for (x, y) in nose_points:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        for (x, y) in mouth_points:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        for (x, y) in jawline_points:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        model = ScoreModel(shape)
        result = model.final_result()
        return result
    # Display the output image

@csrf_exempt
def upload_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        image_pil = Image.open(image_file)
        image_np = np.array(image_pil)

        if image_np.shape[2] == 4:  
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)

        result = scoring_face(image_np)
        result = str(result)
        return JsonResponse({'result': result})
    return JsonResponse({'message': 'Invalid request'}, status=400)
