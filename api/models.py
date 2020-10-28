from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

"""
Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.
"""


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


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False,
                            verbose_name='Категория')
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Жанр')
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100, blank=False,
                            verbose_name='Произведение')
    year = models.PositiveIntegerField(
        default=date.today().year,
        validators=[MaxValueValidator(date.today().year)],
        db_index=True
    )
    description = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True,
                                validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="review"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="review"
    )
    pub_date = models.DateTimeField("review date", auto_now_add=True)
    score = models.IntegerField(null=True, blank=True,
                                validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])

    class Meta:
        unique_together = ['author', 'title']
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Comment(models.Model):
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE,
                                related_name='comments',
                                blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField("comment date", auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
