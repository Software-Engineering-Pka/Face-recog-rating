from django.urls import path
from . import views
app_name = "face_rating_app"
urlpatterns = [
    path('', views.face_rating, name='face_rating'),
]
