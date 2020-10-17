from django.contrib import admin
<<<<<<< HEAD
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    empty_value_display = "-пусто-"


class GenresAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    empty_value_display = "-пусто-"


class TitlesAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", 'description', 'genre', 'category')
    empty_value_display = "-пусто-"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "text", 'author', 'pub_date', 'score')
    empty_value_display = "-пусто-"


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("pk", 'reviews', 'author', 'text', 'pub_date')
    empty_value_display = "-пусто-"


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", 'role', 'username', 'email', 'bio')
    empty_value_display = "-пусто-"


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(User, UserAdmin)
=======

# Register your models here.
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede
