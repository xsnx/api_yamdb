from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, filters, mixins
from rest_framework.viewsets import GenericViewSet
from api.filters import TitleFilter
from api.serializers import CategoriesSerializer, GenresSerializer, \
    ReviewSerializer, TitlesSerializer, CommentSerializer, TitlesEditSerial
from api.permissions import IsAdminOrReadOnly, ReviewCommentPermission
from api.models import Categories, Genres, Titles, Review
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as djfilter

class MixinsViewSets(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     mixins.ListModelMixin, GenericViewSet):
    pass


class CategoryAPIView(MixinsViewSets):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def destroy(self, request, slug):
        del_genre = self.queryset.filter(slug=slug)
        del_genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenresAPIView(MixinsViewSets):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def destroy(self, request, slug):
        del_genre = self.queryset.filter(slug=slug)
        del_genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitlesAPIView(viewsets.ModelViewSet):
    queryset = Titles.objects.annotate(rating=Avg('review__score'))
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    __basic_fields = ('genre', 'category', 'year', 'name')
    filter_backends = (djfilter.DjangoFilterBackend, SearchFilter)
    #filter_fields = __basic_fields
    #search_fields = __basic_fields

    filterset_class = TitleFilter


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesSerializer
        else:
            return TitlesEditSerial


class ReviewAPIView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewCommentPermission]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id')
        )
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentsAPIView(viewsets.ModelViewSet):
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
