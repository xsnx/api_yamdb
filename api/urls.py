from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (CategoryAPIView, CommentsAPIView, GenresAPIView,
                       ReviewAPIViewSet, TitlesAPIView, UserViewSet,
                       reg_user_email, token)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='api_users')
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
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/auth/token/email/', reg_user_email),
    path('v1/auth/token/', token),
    ]
