from django.urls import path
from . import views
app_name = "face_recognition_app"
urlpatterns = [
    path('', views.face_recognition_view, name='face_recognition_app'),
    path('video_feed/', views.video_feed, name='video_feed'),

]
