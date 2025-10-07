# accounts/urls.py
from django.urls import path
from .views import RegisterView, CustomObtainAuthToken, ProfileView, public_profile

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomObtainAuthToken.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),            # current user profile (requires token)
    path("profile/<str:username>/", public_profile, name="public_profile"),  # public profile by username
]
