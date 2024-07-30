from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Post
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import login_required
from .forms import PostForm, SignUpForm, UpdateUserForm, ChangePasswordForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
        messages.success(request, "You are already logged in")
        return redirect('home')
    else:
        form = SignUpForm()

        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                messages.success(request, "User account was created!")
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'An error has occurred during registration')

        return render(request, 'core/register.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_pic = Profile.objects.get(user__id=request.user.id)

        user_form = UpdateUserForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_pic)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, "Your profile has been successfully updated")
            return redirect('home')
        return render(request, "core/update_user.html",
                      {'user_form': user_form, "profile_form": profile_form})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('login')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been successfully changed")
                login(request, current_user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "core/update_password.html", {'form': form})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('login')


def post_like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, "You must be logged in to like that post")
        return redirect('login')


def post_show(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post:
        return render(request, "core/post_show.html", {'post': post})
    else:
        messages.error(request, "That post does not exist")
        return redirect('home')


def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        return redirect(request.META.get('HTTP_REFERER'))


def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        return redirect(request.META.get('HTTP_REFERER'))


def followers(request, pk):
    profiles = Profile.objects.get(user_id=pk)
    return render(request, 'core/followers.html', {'profiles': profiles})


def follows(request, pk):
    profiles = Profile.objects.get(user_id=pk)
    return render(request, 'core/follows.html', {'profiles': profiles})
