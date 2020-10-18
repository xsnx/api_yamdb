from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    confirmation_code = models.CharField(max_length=400, blank=True)
    role = models.CharField(max_length=100)
    password = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=128, blank=False, unique=True)
    bio = models.CharField(max_length=128, blank=True)
