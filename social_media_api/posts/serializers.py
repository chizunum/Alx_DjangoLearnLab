from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


# -------------------------------
# 📝 POST SERIALIZER
# -------------------------------
class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_profile_picture = serializers.ImageField(
        source='author.profile_picture',
        read_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'image',
            'author',
            'author_username',
            'author_profile_picture',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


# -------------------------------
# 💬 COMMENT SERIALIZER
# -------------------------------
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'author_username',
            'content',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
