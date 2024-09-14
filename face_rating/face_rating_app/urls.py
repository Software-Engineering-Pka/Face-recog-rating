from django.urls import path
from . import views
app_name = "face_rating_app"
urlpatterns = [
    path('face_rating/', views.face_rating, name='face_rating'),
    path('', views.home, name='home'),
    path('upload/', views.upload_view, name='upload'),

]
