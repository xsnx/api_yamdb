from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (CategoryAPI, CommentsAPI, GenresAPI,
                       ReviewAPI, TitleAPI, UserViewSet,
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
    CommentsAPI, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/auth/token/email/', reg_user_email),
    path('v1/auth/token/', token),
    ]
