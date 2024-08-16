from rest_framework import serializers

from key_value.users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
        ]

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("password must be at least 8 char")
        return value


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        exclude = [
            "password",
            "is_admin",
            "is_superuser",
        ]
