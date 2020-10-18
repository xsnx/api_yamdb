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
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .pagination import CustomPagination
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = User_Serializer
    permission_classes = [IsAuthenticated, Permission1]
    pagination_class = CustomPagination
    lookup_field = 'username'


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
