from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'full_name', 'profile_pic', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['password_hash'] = make_password(validated_data.pop('password'))
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, write_only=True)