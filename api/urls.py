from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
<<<<<<< HEAD
=======

>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from api.views import *

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
<<<<<<< HEAD
=======
#router.register(r'/auth/email', RegisterUsersView, basename='users')
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede
router.register(r'titles', TitlesAPIView, basename='titles')
router.register(r'categories', CategoryAPIView, basename='categories')
router.register(r'genres', GenresAPIView, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewAPIView,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsAPIView, basename='comments')

<<<<<<< HEAD
urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(),
=======

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(),
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/api-token-auth/', views.obtain_auth_token),
<<<<<<< HEAD
    path('v1/auth/email/', RegisterUsersView.as_view()),
    path('v1/', include(router.urls)),
]
=======
    #path('v1/auth/email/', RegisterUsersView.as_view()),
    path('v1/', include(router.urls)),

]
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede
