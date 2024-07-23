from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Post
# from django.contrib.auth.decorators import login_required
from .forms import PostForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
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


# @login_required(login_url='login')
def profile_list(request):
    profiles = Profile.objects.exclude()
    return render(request, 'core/profile_list.html', {'profiles': profiles})


# @login_required(login_url='login')
def profile(request, pk):
    profile = Profile.objects.get(user_id=pk)
    posts = Post.objects.filter(user_id=pk).order_by("-created_at")
    # Post Form logic
    if request.method == "POST":
        # Get current user ID
        current_user_profile = request.user.profile
        #  Get form data
        action = request.POST['follow']

        # Decide to follow or unfollow
        if action == "unfollow":
            current_user_profile.follows.remove(profile)
        else:
            current_user_profile.follows.add(profile)
        # Save the profile
        current_user_profile.save()
    return render(request, 'core/profile.html', {'profile': profile, 'posts': posts})


def login_user(request):
    if request.user.is_authenticated:
        messages.success(request, "You're already logged in")
        return redirect('home')
    else:

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been successfully logged in")
                return redirect('home')
            else:
                messages.success(request, "There was ann error logging in. Please try again")
                return redirect('login')
        else:
            return render(request, 'core/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        messages.success(request, "You're already logged in")
        return redirect('home')
    else:
        page = 'register'
        form = SignUpForm()

        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()

                messages.success(request, "User account was created!")
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'An error has occurred during registration')

        context = {'page': page, 'form': form}

    return render(request, 'core/register.html', context)
