from django_filters import rest_framework as filters
import django_filters
from api.models import Genres, Titles, Categories


class GenreFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='iexact'
    )

    class Meta:
        model = Titles
        fields = ['id', 'name', 'year', 'description', 'genre',
                  'category']