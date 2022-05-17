from tkinter import CASCADE
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
    is_open = models.BooleanField(default=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Comments(models.Model):
    comment = models.TextField(max_length=600)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)