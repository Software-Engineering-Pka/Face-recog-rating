from django.contrib import admin
from .models import RatingSessionsModel,RatingModel
# Register your models here.
admin.site.register(RatingModel)
admin.site.register(RatingSessionsModel)