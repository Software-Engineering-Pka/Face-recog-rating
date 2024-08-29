from django.db import models

# Create your models here.
class FaceModel(models.Model):
    image = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    