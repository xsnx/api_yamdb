from datetime import date

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

"""
Ресурс TITLE: произведения, к которым пишут отзывы (определённый фильм, книга
или песенка).
Ресурс CATEGORY: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
Ресурс GENRE: жанры произведений. Одно произведение может быть привязано к
нескольким жанрам.
Ресурс REVIEW: отзывы на произведения. Отзыв привязан к определённому
произведению.
Ресурс COMMENT: комментарии к отзывам. Комментарий привязан к определённому
отзыву.
"""


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Genre'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100, blank=False)
    year = models.PositiveIntegerField(
        default=date.today().year,
        validators=[MaxValueValidator(date.today().year)]
    )
    description = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True,
                                validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Title'

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

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ['author', 'title']
        ordering = ['-pub_date']


class Comment(models.Model):
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE,
                                related_name='comments', blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField("comment date", auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Comment'

    def __str__(self):
        return self.text
