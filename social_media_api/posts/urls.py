from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, like_post, unlike_post


# -----------------------------
# 🔹 ROUTER SETUP
# -----------------------------
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

# -----------------------------
# 🔹 URL PATTERNS
# -----------------------------
urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', like_post, name='post-like'),
    path('posts/<int:pk>/unlike/', unlike_post, name='post-unlike'),
]
