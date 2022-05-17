from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listings(models.Model):
    title = models.CharField(max_length=30)
    bids = models.IntegerField()
    description = models.TextField(max_length=400)
    img_url = models.CharField(max_length=200)
    category = models.CharField(max_length=20)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
