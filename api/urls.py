from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from api.views import *

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
#router.register(r'/auth/email', RegisterUsersView, basename='users')
router.register(r'titles', TitlesAPIView, basename='titles')
router.register(r'categories', CategoryAPIView, basename='categories')
router.register(r'genres', GenresAPIView, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewAPIView,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsAPIView, basename='comments')


urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/api-token-auth/', views.obtain_auth_token),
    #path('v1/auth/email/', RegisterUsersView.as_view()),
    path('v1/', include(router.urls)),

]