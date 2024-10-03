from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from .models import AccountModel
from django.contrib.auth import login,authenticate,logout

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from face_recognition_app.face_recog_model import face_recog_model
import os
from django.conf import settings
import cv2
from django.views.decorators.csrf import csrf_exempt
import base64
import json
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
from io import BytesIO
from PIL import Image
import numpy as np
from face_recognition_app.views import close_camera
def signup(request):
    close_camera()
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("face_rating_app:face_rating")
    else:
        form = SignUpForm()
    
    context = {
        "form":form
    }
    return render(request,"account/signup.html",context)

def signin(request):
    close_camera()
    next = request.GET.get("next")
    form =SignInForm()
    if request.method == 'POST':
        email_login = request.POST.get("email")
        password_login = request.POST.get("password")
        form = SignInForm(request, data=request.POST)
        user = authenticate(request, username=email_login, password=password_login)
        if user is not None:
            login(request, user)
            if next:
                return redirect(next)
            return redirect('face_rating_app:face_rating')
       
    context = {
        "form":form
    }
    return render(request,"account/signin.html",context)
def signout(request):
    close_camera()
    logout(request)
    return redirect("account:signin")

def face_id_to_login(request):
    close_camera()
    if request.method == "POST":
        try:
            base64_string = request.POST.get("imageData")
            header, base64_data = base64_string.split(';base64,')
            image_data = base64.b64decode(base64_data)

            # Chuyển đổi dữ liệu base64 thành ảnh sử dụng OpenCV
            image = np.array(Image.open(BytesIO(image_data)))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Chuyển đổi màu từ RGB sang BGR nếu cần

            # Đọc ảnh bằng OpenCV
            recog_face_model = face_recog_model()
            recog_face_model.encoding_faces()

            try:
                # So sánh khuôn mặt trong ảnh với các khuôn mặt đã lưu
                coors, names = recog_face_model.comparing_faces(image)
                account = AccountModel.objects.get(username=names[0])

                if account:
                    login(request, account)
                    return redirect('face_rating_app:face_rating')
            except Exception as e:
                print('Lỗi nhận diện hoặc đăng nhập:', e)
                return JsonResponse({'error': 'Face recognition failed'}, status=500)

            return JsonResponse({'error': 'Invalid image path'}, status=400)
        except Exception as e:
            print('An exception occurred:', e)
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    # Xử lý trường hợp không phải POST
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def face_id(request):
    close_camera()
    return render(request, "account/face_id.html")
