from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import TitlesAPIView, CategoryAPIView, GenresAPIView, \
    ReviewAPIView, CommentsAPIView

router = DefaultRouter()
router.register(r'titles', TitlesAPIView, basename='titles')
router.register(r'categories', CategoryAPIView, basename='categories')
router.register(r'genres', GenresAPIView, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewAPIView,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsAPIView, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
