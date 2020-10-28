from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (
    CategoryAPI, CommentAPI, GenresAPI, ReviewAPI, TitleAPI, UserViewSet,
    reg_user_email, token)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='api_users')
router.register(r'titles', TitleAPI, basename='titles')
router.register(r'categories', CategoryAPI, basename='categories')
router.register(r'genres', GenresAPI, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewAPI,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentAPI, basename='comments')

authorization = [
    path('refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('email/', reg_user_email),
    path('', token),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', include(authorization)),
]
