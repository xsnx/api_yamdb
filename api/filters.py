from django_filters import rest_framework as filters
import django_filters
from api.models import Genres, Titles, Categories


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='iexact'
    )
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='iexact')
    name = django_filters.CharFilter(field_name="name", lookup_expr="contains")


    class Meta:
        model = Titles
        fields = ('genre','category', 'year', 'name',)
        #fields = '__all__'
        #fields = ['genre', 'id','category'] #'genre'] 'year''description','name'