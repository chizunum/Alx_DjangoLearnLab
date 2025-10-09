from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

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
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()

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
            "likes_count", 
            "is_liked_by_user",
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
 

    def get_is_liked_by_user(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False


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

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]