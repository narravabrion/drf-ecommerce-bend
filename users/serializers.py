from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(
        max_length=40,
        min_length=5,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_lowercase,
            validate_password_symbol,
            validate_password_uppercase,
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "is_active",
            "is_verified",
            "is_staff",
            "is_superuser",
        )
