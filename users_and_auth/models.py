from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = [('user', 'user'),
             ('moderator', 'moderator'),
             ('admin', 'admin'),
             ]
    confirmation_code = models.CharField(
        max_length=400,
        unique=True, 
        editable=False,
        null=True, 
        blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    password = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=128, blank=False, unique=True)
    bio = models.CharField(max_length=128, blank=True)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
