from django.urls import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from users.models import Profile


@login_required(login_url='login')
def add_post(request):
    form = PostForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your post has been created")
            return redirect(reverse('profile', args=[request.user.id]))
    posts = Post.objects.all().order_by("-created_at")
    return render(request, 'posts/add_post.html', {'posts': posts, 'form': form})


def post_like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You must be logged in to like that post")
        return redirect('login')


def delete_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if request.user.username == post.user.username:
            post.delete()
            messages.success(request, "The post has been deleted")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You must be logged in")
        return redirect('login')


def edit_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if request.user.username == post.user.username:
            form = PostForm(request.POST, request.FILES, instance=post)
            if request.method == 'POST':
                if form.is_valid():
                    post = form.save(commit=False)
                    post.user = request.user
                    post.save()
                    messages.success(request, "Your post has been updated")
                    return redirect(reverse('profile', args=[request.user.id]))
            else:
                return render(request, "posts/edit_post.html", {'form': form, "post": post})
        else:
            messages.error(request, "You can't edit a post that is not yours!")
            return redirect('home')

    else:
        messages.error(request, "You must be logged in")
        return redirect('login')


def posts_follows(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, "Your post has been created")
                return redirect('posts_follows')

        profile = get_object_or_404(Profile, user=request.user)
        follows = profile.follows.all()

        print(f"Following users: {list(follows)}")
        posts = Post.objects.filter(user__in=follows.values_list('user_id')).order_by('-created_at')

        return render(request, 'posts/posts_follows.html', {'posts': posts, 'form': form})
    else:
        messages.error(request, "You are not allowed to view that page")
        return redirect("login")