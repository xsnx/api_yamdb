from .models import User
from .serializer import User_Serializer
from .permissions import Permission1
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated)
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .pagination import CustomPagination
from rest_framework import status
from django.core.mail import send_mail
import random


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = User_Serializer
    permission_classes = [IsAuthenticated, Permission1]
    pagination_class = CustomPagination
    lookup_field = 'username'


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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


@api_view(('POST',))
def token(request):
    email = request.data.get('email')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(
        User, email=email, confirmation_code=confirmation_code)
    tokens = get_tokens_for_user(user)
    return Response({"message": tokens})


@api_view(('POST',))
def reg_user_email(request):
    if not request.data.get('email'):
        return Response({'message': {
            'Ошибка': 'Не указана почта для регистрации'}})
    try:
        email = request.data.get('email')
        a = get_user_model().objects.filter(email=email)
    except:
        return Response({'message': {
            'Ошибка': 'Пользователь с такой почтой уже зарегистрирован'}})
    email = request.data.get('email')
    confirmation_code = random.randint(200, 1000)
    try:
        get_user_model().objects.create(email=email, username=email)
    except:
        return Response({'message': {
            'Ошибка': 'Чего-то не создался пользователь'}})
    send_mail(
        'Подтверждение адреса электронной почты YaTube',
        'Вы получили это письмо, потому что регистрируетесь на ресурсе '
        'YaTube Код подтверждения confirmation_code=' + str(confirmation_code),
        'info@yatube.ru',
        [email,],
        fail_silently=False,)
    return Response({'message': {
        'ОК': f'Пользователь c email {email} создан успешно. '
        'Код подтверждения отправлен на электронную почту'}})
