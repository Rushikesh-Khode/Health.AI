from django.db import models


# Create your models here.

class Gender(models.Model):
    type = models.CharField(max_length=10, null=True)


class User(models.Model):
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(null=False, max_length=256)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING)
    birthday = models.DateField()
    phone_no = models.CharField(max_length=20)
    x_auth_token = models.CharField(null=True, max_length=256)
    x_auth_created_at = models.DateTimeField(null=True)
