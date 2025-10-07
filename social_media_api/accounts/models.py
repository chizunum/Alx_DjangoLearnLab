from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# accounts/models.py


def user_profile_image_path(instance, filename):
    return f"profile_pics/user_{instance.id}/{filename}"

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_image_path, blank=True, null=True
    )
    # followers - ManyToMany to self, non-symmetrical (A follows B != B follows A)
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",  # users that this user is following will be accessible via .following
        blank=True,
    )

    def __str__(self):
        return self.username
