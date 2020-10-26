from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryAPIView, CommentsAPIView, GenresAPIView,
                       ReviewAPIViewSet, TitlesAPIView)

router = DefaultRouter()
router.register(r'titles', TitlesAPIView, basename='titles')
router.register(r'categories', CategoryAPIView, basename='categories')
router.register(r'genres', GenresAPIView, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewAPIViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsAPIView, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
