from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'role', 'email', 'confirmation_code',
                  'password', 'bio', 'first_name', 'last_name')
        model = get_user_model()


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username',
                  'password', 'bio', 'first_name', 'last_name')
        model = get_user_model()
