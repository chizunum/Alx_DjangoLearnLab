from rest_framework import viewsets, permissions, generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view
 
User = get_user_model()

# -----------------------------
# 🔹 PAGINATION
# -----------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# -----------------------------
# 👤 USER VIEWSET
# -----------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.follow(target_user)
        return Response({"detail": f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        request.user.unfollow(target_user)
        return Response({"detail": f"You unfollowed {target_user.username}."}, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class CustomObtainAuthToken(ObtainAuthToken):
    """Custom token authentication to return token + user info."""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        })

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Allows the authenticated user to view and update their own profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['GET'])
def public_profile(request, username):
    """Return the public profile of a user by username."""
    user = get_object_or_404(User, username=username)
    serializer = UserSerializer(user, context={'request': request})
    return Response(serializer.data)