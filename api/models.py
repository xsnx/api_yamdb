from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

#User = get_user_model()

"""
Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.
"""

class User(AbstractUser):
    ROLES = [('user', 'user'),
             ('moderator', 'moderator'),
             ('admin', 'admin'),
             ]
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    confirmation_code = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username

class Categories(models.Model):
    name = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=100, blank=False)
    year = models.PositiveIntegerField(
        default=date.today().year,
        validators=[MaxValueValidator(date.today().year)]
    )
    description = models.TextField(null=True, blank=True)
    #rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    genre = models.ManyToManyField(Genres, verbose_name='genre')
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles_of_category',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def get_genres(self):
        return "\n".join([i.name for i in self.genre.all()])


class Review(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    pub_date = models.DateTimeField("Дата отзыва", auto_now_add=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    #rating = RatingField(range=10)

    def __str__(self):
        return self.text

    class Meta:
        #unique_together = ['author', 'title']
        ordering = ['-pub_date']


class Comments(models.Model):
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE,
                                related_name='reviews', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['created']


