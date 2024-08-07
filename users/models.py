from django.db import models
from django.contrib.auth.models import User


# User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    bio = models.CharField(null=True, blank=True, max_length=500)

    def __str__(self):
        return self.user.username
