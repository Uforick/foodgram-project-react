from rest_framework import serializer
from .models import User


class UserSerializer(serializer.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
