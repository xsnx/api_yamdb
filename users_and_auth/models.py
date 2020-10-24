from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = [('user', 'user'),
             ('moderator', 'moderator'),
             ('admin', 'admin'),
             ]
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    confirmation_code = models.CharField(max_length=300, blank=True)
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.username