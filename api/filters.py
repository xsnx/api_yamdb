import django_filters
from api.models import Titles


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='iexact'
    )
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact'
    )
    #name = django_filters.CharFilter(field_name='name')

    class Meta:
        model = Titles
        # fields = (
        #     'genre',
        #     'category',
        #     'year',
        #     'name',
        # )
        fields = {
            'genre': ['exact'],
            'category': ['exact'],
            'year': ['exact'],
            'name': ['exact'],
        }
