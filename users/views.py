from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .models import Profile
from posts.models import Post
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def profiles(request):
    profiles = Profile.objects.exclude()
    return render(request, 'users/profiles.html', {'profiles': profiles})


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
    return render(request, 'users/profile.html', {'profile': profile, 'posts': posts})


def login_user(request):
    if request.user.is_authenticated:
        messages.error(request, "You're already logged in")
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
                messages.error(request, "There was ann error logging in. Please try again")
                return redirect('login')
        else:
            return render(request, 'users/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('login')


def register_user(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in")
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

        return render(request, 'users/register.html', {'form': form})


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
            return redirect(reverse('profile', args=[request.user.id]))
        return render(request, "users/update_user.html",
                      {'user_form': user_form, "profile_form": profile_form})
    else:
        messages.error(request, "You must be logged in to view that page")
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
                return redirect(reverse('profile', args=[request.user.id]))
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "users/update_password.html", {'form': form})
    else:
        messages.error(request, "You must be logged in to view that page")
        return redirect('login')


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
    return render(request, 'users/followers.html', {'profiles': profiles})


def follows(request, pk):
    profiles = Profile.objects.get(user_id=pk)
    return render(request, 'users/follows.html', {'profiles': profiles})
