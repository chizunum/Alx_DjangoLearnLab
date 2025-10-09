from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from notifications.models import Notification

# -----------------------------
# 🔹 PAGINATION
# -----------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# -----------------------------
# 📝 POSTS VIEWSET
# -----------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").prefetch_related("comments").all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["author__username"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -----------------------------
# 💬 COMMENTS VIEWSET
# -----------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["post", "author__username"]
    search_fields = ["content"]
    ordering_fields = ["created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -----------------------------
# 📰 FEED VIEW
# -----------------------------
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        # Include posts from followed users + current user
        return (
            Post.objects.filter(author__in=list(following_users) + [user])
            .select_related("author")
            .order_by("-created_at")
        )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    """Like a post and create a notification for the post author (if not the liker)."""
    user = request.user
    post = get_object_or_404(Post, pk=pk)

    if post.author == user:
        # Optionally allow liking your own post or not; here we allow but still unique constraint will hold.
        pass

    try:
        with transaction.atomic():
            like, created = Like.objects.get_or_create(post=post, user=user)
            if not created:
                return Response({"detail": "Already liked."}, status=status.HTTP_400_BAD_REQUEST)

            # create notification (skip if actor == recipient)
            if post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb="liked your post",
                    target_content_type=ContentType.objects.get_for_model(Post),
                    target_object_id=str(post.pk),
                )

            return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({"detail": "Could not like post."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=pk)
    deleted, _ = Like.objects.filter(post=post, user=user).delete()
    # Optionally create a "unliked" notification (usually not needed)
    return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)