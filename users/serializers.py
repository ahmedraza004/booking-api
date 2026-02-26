# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import password_validation
from rest_framework.validators import UniqueValidator
from .models import CustomUser
import re

User = CustomUser

PHONE_REGEX = re.compile(r'^\+?[0-9\- ]{7,20}$')

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number']
        read_only_fields = ['id', 'role', 'username', 'email']  # prevent self-escalation

class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']  # users can change these only

    def validate_phone_number(self, v):
        if v and not PHONE_REGEX.match(v):
            raise serializers.ValidationError("Invalid phone number format.")
        return v

class SignupSerializer(serializers.ModelSerializer):
    # Do not allow client to set role; keep default on model.
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all(), lookup='iexact')],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), lookup='iexact')],
    )
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password']

    def validate_username(self, v):
        v = v.strip().lower()
        return v

    def validate_email(self, v):
        return v.strip().lower()

    def validate_phone_number(self, v):
        if v and not PHONE_REGEX.match(v):
            raise serializers.ValidationError("Invalid phone number format.")
        return v

    def validate(self, attrs):
        # Use Django’s built-in password validators
        password = attrs.get('password')
        user = User(username=attrs.get('username'), email=attrs.get('email'))
        password_validation.validate_password(password, user=user)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user