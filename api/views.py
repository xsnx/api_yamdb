from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from api.models import Category, Genre, Review, Title
from api.permissions import (IsAdminOrReadOnly, ReviewCommentPermission)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer)

from .filters import TitleFilter


class MixinViewSets(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                    mixins.ListModelMixin, GenericViewSet):
    pass


class CategoryAPIView(MixinViewSets):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class GenreAPIView(MixinViewSets):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class TitleAPIView(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('review__score'))
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    __basic_fields = ('genre', 'category', 'year', 'name')
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = __basic_fields
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewCommentPermission]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentAPIView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewCommentPermission]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"), )
        return queryset.comments.all()

    def perform_create(self, serializer):
        reviews = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"), )
        serializer.save(
            author=self.request.user,
            reviews=reviews
        )
