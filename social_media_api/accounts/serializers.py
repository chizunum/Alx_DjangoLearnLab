from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "profile_picture",
            "followers_count",
            "following_count",
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "bio",
            "profile_picture",
            "token",
        ]

    def create(self, validated_data):
        # Extract and hash password properly
        password = validated_data.pop("password")
        user = get_user_model().objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            password=password,
            bio=validated_data.get("bio", ""),
            profile_picture=validated_data.get("profile_picture", None),
        )

        # Create token for authentication
        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key  # attach for serializer output
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
