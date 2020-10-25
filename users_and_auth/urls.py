#from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import UserMeView, UserViewSet, get, token

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='api_users')

urlpatterns = [
    path('', get),
    path('v1/auth/token/', TokenObtainPairView.as_view()), #token),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/users/me/', UserMeView.as_view()),
    path('v1/', include(router.urls)),
]
