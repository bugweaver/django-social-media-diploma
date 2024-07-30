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


# Post Model
class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)

    def count_likes(self):
        return self.likes.count()

    def __str__(self):
        return (f'{self.user}'
                f' ({self.created_at:%Y-%m-%d %H:%M}) '
                f'{self.body}...')
