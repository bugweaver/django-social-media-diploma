from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from posts.models import Post
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import login_required
from posts.forms import PostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms


def home(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, "Your post has been created")
                return redirect('home')
        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'core/home.html', {'posts': posts, 'form': form})
    else:
        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'core/home.html', {'posts': posts})


