from django.urls import path
from .views import (
    RegisterView,
    CustomObtainAuthToken,
    ProfileView,
    public_profile,
    FollowUserView,
    UnfollowUserView,
)

urlpatterns = [
    # 🔹 Authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomObtainAuthToken.as_view(), name="login"),

    # 🔹 Profile Management
    path("profile/", ProfileView.as_view(), name="profile"),                 # Current user's profile
    path("user/<str:username>/", public_profile, name="public-profile"),     # Public profile by username

    # 🔹 Follow System
    path("follow/<int:user_id>/", FollowUserView.as_view(), name="follow-user"),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view(), name="unfollow-user"),
]
