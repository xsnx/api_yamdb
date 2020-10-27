from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', _('user')
        MODERATOR = 'moderator', _('moderator')
        ADMIN = 'admin', _('admin')

    confirmation_code = models.CharField(
        max_length=400,
        unique=True,
        editable=False,
        null=True,
        blank=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER)
    password = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=128, blank=False, unique=True)
    bio = models.CharField(max_length=128, blank=True)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR
