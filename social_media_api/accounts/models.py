from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Helper function for profile picture uploads
def user_profile_image_path(instance, filename):
    return f"profile_pics/user_{instance.id}/{filename}"


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_image_path, blank=True, null=True
    )

    # Users this user follows (non-symmetrical relationship)
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
        help_text="Users that this user is following"
    )

    def __str__(self):
        return self.username

    # ---- Helper methods for follow system ----
    def follow(self, user):
        """Follow another user."""
        if user == self:
            raise ValueError("You cannot follow yourself.")
        self.following.add(user)

    def unfollow(self, user):
        """Unfollow a user."""
        self.following.remove(user)

    def is_following(self, user):
        """Check if this user follows another user."""
        return self.following.filter(pk=user.pk).exists()
