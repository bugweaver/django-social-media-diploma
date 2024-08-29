from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)

    def count_likes(self):
        return self.likes.count()

    def total_comments_and_replies(self):
        comments_count = self.comments.count()
        replies_count = sum(comment.replies.count() for comment in self.comments.all())
        return comments_count + replies_count

    def __str__(self):
        return (f'{self.user}'
                f' ({self.created_at:%Y-%m-%d %H:%M}) '
                f'{self.body}...')
