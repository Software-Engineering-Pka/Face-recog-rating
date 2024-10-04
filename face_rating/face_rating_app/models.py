from django.db import models
from account.models import AccountModel

class RatingSessionsModel(models.Model):
    account = models.ForeignKey(AccountModel, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id} - {self.created_at}"

class RatingModel(models.Model):
    session = models.ForeignKey(RatingSessionsModel, on_delete=models.CASCADE)
    eye_point = models.FloatField()
    nose_point = models.FloatField()
    jawline_point = models.FloatField()
    mouth_point = models.FloatField()
    mean_point = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Rating for {self.session}"
