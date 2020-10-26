from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserMeView, UserViewSet, reg_user_email, token

urlpatterns = [
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(),
        name='token_refresh'),
    path('v1/auth/token/email/', reg_user_email),
    path('v1/auth/token/', token),
    path('v1/users/me/', UserMeView.as_view()),
    ]
router = DefaultRouter()
router.register(r'users',
    UserViewSet, basename='api_users')
urlpatterns += [
    path('v1/', include(router.urls)),
    ]
