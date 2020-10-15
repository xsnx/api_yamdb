from .models import User
from .serializer import User_Serializer
from .permissions import Permission1
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissionsOrAnonReadOnly,
    AllowAny)
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .pagination import CustomPagination

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = User_Serializer
    permission_classes = [IsAuthenticated,]
    pagination_class = CustomPagination 

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Username', 'email']
    objects = ''


    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserMyViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = User_Serializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email']


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class GetTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    @api_view(('POST',))
    def post(self, request):
        email = request.data.get('email')
        print(email)
        user = get_object_or_404(User, email=email)
        code = request.data.get('confirmation_code')
        if user.confirmation_code == code:
            tokens = get_tokens_for_user(user)
            return Response({"message": tokens})
        return Response({"message": "неверный код подтверждения."})

@api_view(('GET',))
def get(request):
    data = {'aaa': 'AAA'}
    users = get_user_model().objects.all()
    print(users)
    seria = User_Serializer(users, many=True)

    return Response(seria.data)

@api_view(('POST',))
def token(request):
    email = request.data.get('email')
    print(email)
    user = get_object_or_404(User, email=email)
    seria = User_Serializer(user, many=False)
    tokens = get_tokens_for_user(user)
    return Response({"message": tokens})
