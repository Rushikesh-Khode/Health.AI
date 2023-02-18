from django.db import models
from users.models import User


class Predictions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.TextField(max_length=7000, null=False)
    createdAt = models.DateTimeField(auto_now=True)
    glioma = models.FloatField(default=0.0, null=False)
    meningioma = models.FloatField(default=0.0, null=False)
    no_tumor = models.FloatField(default=0.0, null=False)
    pituitary = models.FloatField(default=0.0, null=False)
