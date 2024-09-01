from django.shortcuts import render

# Create your views here.
def face_rating(request):
    return render(request,"face_rating_app/index.html")