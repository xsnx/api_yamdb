from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()

"""
Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.
"""


class Categories(models.Model):
    name = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=100, blank=False)
    year = models.PositiveIntegerField(
        default=date.today().year,
        validators=[MaxValueValidator(date.today().year)]
    )
    description = models.TextField(null=True, blank=True)
    #score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        related_name="titles_of_genre",
        blank=True,
        null=True,
    )
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
        related_name="review"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="review"
    )
    pub_date = models.DateTimeField("Дата отзыва", auto_now_add=True)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    # rating = RatingField(range=10)

    def __str__(self):
        return self.text

    class Meta:
        # unique_together = ['author', 'title']
        ordering = ['-pub_date']


class Comments(models.Model):
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE,
                                related_name='review', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['created']
