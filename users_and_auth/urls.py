from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
    
urlpatterns = [
        path('', views.get),
        # path('v1/auth/token/', views.GetTokenAPIView.as_view(), name='token_obtain_pair'),
        path('v1/auth/token/', views.token),


        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        # path('email/', Reg_user.as_view(), name='reg_user'),
    ]







router = DefaultRouter()
router.register(r'users',
    views.UserViewSet, basename='api_users')
router.register(r'users/my',
    views.UserMyViewSet, basename='api_users_my')



urlpatterns += [
    path('v1/', include(router.urls)),
    ]
