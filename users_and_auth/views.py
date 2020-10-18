from .models import User
from .serializer import User_Serializer
from .permissions import Permission1, Permission2
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
from .pagination import CustomPagination, CustomPagination1
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = User_Serializer
    permission_classes = [IsAuthenticated, Permission1]
    pagination_class = CustomPagination
    lookup_field = 'username'

    # def get_object(self):
    #     if self.kwargs.get('username') == 'me':
    #         obj = self.request.user

    #         return obj
    #     else:
    #         queryset = self.filter_queryset(self.get_queryset())
    #         lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
    #         assert lookup_url_kwarg in self.kwargs, (
    #             'Expected view %s to be called with a URL keyword argument '
    #             'named "%s". Fix your URL conf, or set the `.lookup_field` '
    #             'attribute on the view correctly.' %
    #             (self.__class__.__name__, lookup_url_kwarg)
    #         )
    #         filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
    #         obj = get_object_or_404(queryset, **filter_kwargs)
    #         self.check_object_permissions(self.request, obj)

    #         return obj

    # def get_queryset(self):
    #     if self.kwargs.get('username') == 'me':

    #         username = self.request.user.username
    #         queryset = get_user_model().objects.filter(
    #             username=username)
    #         print(f'вывести текущего пользователя {queryset}')
    #         return queryset
    #     if self.kwargs.get('username') is None:
    #         queryset = get_user_model().objects.all()
    #         print('вывести все объекты')
    #         return queryset
    #     else:
    #         username = self.kwargs.get('username')
    #         queryset = get_user_model().objects.filter(
    #             username=username)
    #         print(f'вывести 1 объект {a}')
    #         print(queryset)
    #         return queryset
    
    # def list(self, request, *args, **kwargs):
    #     if self.request.user.role not in ('admin',):
    #         print(f'Роль Usera - {self.request.user.role}')
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     queryset = self.filter_queryset(self.get_queryset())

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)    
    #     return Response(serializer.data)

class UserMeView(APIView):
    
    def get(self, request):
        if request.user is None or not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = request.user
            print(user)
            serializer = User_Serializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
    def patch(self, request):
        user = request.user
        serializer = User_Serializer(
            user, data=request.data, many=False, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


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
