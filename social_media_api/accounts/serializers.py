from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


# ------------------------------------
# 1️⃣ User Serializer (Full Details)
# ------------------------------------
class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

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
            "is_following",
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get("request", None)
        if not request or request.user.is_anonymous:
            return False
        return request.user.is_following(obj)


# ------------------------------------
# 2️⃣ Simple User Serializer (Lightweight)
# ------------------------------------
class SimpleUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "followers_count",
            "following_count",
            "is_following",
        )

    def get_is_following(self, obj):
        request = self.context.get("request", None)
        if not request or request.user.is_anonymous:
            return False
        return request.user.is_following(obj)


# ------------------------------------
# 3️⃣ Registration Serializer
# ------------------------------------
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
        password = validated_data.pop("password")
        user = get_user_model().objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            password=password,
            bio=validated_data.get("bio", ""),
            profile_picture=validated_data.get("profile_picture", None),
        )

        # ✅ Generate authentication token
        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        return user


# ------------------------------------
# 4️⃣ Login Serializer
# ------------------------------------
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
