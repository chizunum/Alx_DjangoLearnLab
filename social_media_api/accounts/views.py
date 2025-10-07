from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # token was created in serializer.create; fetch or create to be safe
            token, _ = Token.objects.get_or_create(user=user)
            data = UserSerializer(user, context={"request": request}).data
            # include token in response
            data["token"] = token.key
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Use DRF-provided view for login to return token
class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # super returns {'token': '...'} but we also want user info
        token_key = response.data.get("token")
        token = Token.objects.get(key=token_key)
        user = token.user
        user_data = UserSerializer(user, context={"request": request}).data
        user_data["token"] = token.key
        return Response(user_data)

# Profile view: get or update current user's profile
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Example public user profile by username
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def public_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"detail": "Not found"}, status=404)
    serializer = UserSerializer(user, context={"request": request})
    return Response(serializer.data)
