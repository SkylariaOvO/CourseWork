from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profile_pics/", default="profile_pics/default.png")
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

