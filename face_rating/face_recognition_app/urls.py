from django.urls import path
from . import views
app_name = "face_recognition_app"
urlpatterns = [
    path('face_login/', views.face_recognition_view, name='face_recognition_app'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('stop_webcam/', views.stop_webcam, name='stop_webcam'),

]
