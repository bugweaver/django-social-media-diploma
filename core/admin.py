from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile, Post, Comment

# Unregister Groups
admin.site.unregister(Group)

# Register Profile
admin.site.register(Profile)

# Register Post
admin.site.register(Post)

# Register Comment
admin.site.register(Comment)

# Combine Profile and User
# class ProfileInline(admin.StackedInline):
#     model = Profile


