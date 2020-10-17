from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserMeView, UserViewSet, get, token
    
urlpatterns = [
        path('', get),
        path('v1/auth/token/', token),
        path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('v1/users/me/', UserMeView.as_view()),
    ]
router = DefaultRouter()
router.register(r'users',
    UserViewSet, basename='api_users')   
urlpatterns += [
    path('v1/', include(router.urls)),
    ]

print(urlpatterns)
