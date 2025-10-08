# accounts/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    SimpleUserSerializer,
)

User = get_user_model()


# ------------------------------
# 1️⃣ Register View
# ------------------------------
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            data = UserSerializer(user, context={"request": request}).data
            data["token"] = token.key
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------
# 2️⃣ Custom Login (Token Authentication)
# ------------------------------
class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_key = response.data.get("token")
        token = Token.objects.get(key=token_key)
        user = token.user
        user_data = UserSerializer(user, context={"request": request}).data
        user_data["token"] = token.key
        return Response(user_data)


# ------------------------------
# 3️⃣ Authenticated User Profile (GET / PUT)
# ------------------------------
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------
# 4️⃣ Public Profile by Username (for viewing other users)
# ------------------------------
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def public_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, context={"request": request})
    return Response(serializer.data)


# ------------------------------
# 5️⃣ Follow / Unfollow System
# ------------------------------
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)

        if target == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.user.is_following(target):
            serializer = SimpleUserSerializer(target, context={"request": request})
            return Response(
                {"detail": "Already following.", "user": serializer.data},
                status=status.HTTP_200_OK,
            )

        request.user.follow(target)
        serializer = SimpleUserSerializer(target, context={"request": request})
        return Response(
            {"detail": "Followed successfully.", "user": serializer.data},
            status=status.HTTP_200_OK,
        )


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)

        if target == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.user.is_following(target):
            serializer = SimpleUserSerializer(target, context={"request": request})
            return Response(
                {"detail": "Not following.", "user": serializer.data},
                status=status.HTTP_200_OK,
            )

        request.user.unfollow(target)
        serializer = SimpleUserSerializer(target, context={"request": request})
        return Response(
            {"detail": "Unfollowed successfully.", "user": serializer.data},
            status=status.HTTP_200_OK,
        )
