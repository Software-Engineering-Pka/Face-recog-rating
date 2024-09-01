
from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "account"
urlpatterns = [
    path("signup/",views.signup,name="signup"),
    path("signin/",views.signin,name="signin"),
    path("signout/",views.signout,name="signout"),
    path("face-id/",views.face_id,name="face_id"),
    path("face_login/",views.face_id_to_login,name="face_login"),
]
