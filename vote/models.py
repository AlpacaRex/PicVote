from django.db import models


# Create your models here.
class User(models.Model):
    openid = models.CharField(max_length=50, primary_key=True)
