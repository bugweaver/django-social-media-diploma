from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from posts.models import Post
from posts.forms import PostForm
from users.models import Profile


def home(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, 'core/home.html', {'posts': posts})

