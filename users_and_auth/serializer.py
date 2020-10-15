from rest_framework import serializers
from django.contrib.auth import get_user_model



class User_Serializer(serializers.ModelSerializer):
    # email = serializers.CharField(
    #     read_only=True
    # )
    

    class Meta:
        fields = ('__all__')
        model = get_user_model()