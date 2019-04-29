from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.

class User(AbstractUser):
    phone = models.TextField()
    avatar = models.TextField(max_length=100, blank=True)
