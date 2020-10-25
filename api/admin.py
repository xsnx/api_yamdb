from django.contrib import admin

from .models import *

User = get_user_model()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    empty_value_display = "-пусто-"


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", 'description', 'genre', 'category')
    empty_value_display = "-пусто-"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "text", 'author', 'pub_date', 'score')
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", 'reviews', 'author', 'text', 'pub_date')
    empty_value_display = "-пусто-"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
