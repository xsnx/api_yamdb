from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import *

router = DefaultRouter()
router.register(r'titles', TitleAPIView, basename='titles')
router.register(r'categories', CategoryAPIView, basename='categories')
router.register(r'genres', GenreAPIView, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentAPIView, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
