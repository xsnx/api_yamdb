import django_filters
from .models import *


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='iexact')
 #   category = django_filters.CharFilter(
  #      field_name='category__slug', lookup_expr='iexact')

    class Meta:
        model = Titles
        fields = ['genre']#, 'category']

