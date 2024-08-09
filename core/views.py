from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from posts.models import Post
from posts.forms import PostForm
from users.models import Profile


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

        return render(request, 'core/posts_follows.html', {'posts': posts, 'form': form})
    else:
        posts = Post.objects.none()
        return render(request, 'core/posts_follows.html', {'posts': posts})
