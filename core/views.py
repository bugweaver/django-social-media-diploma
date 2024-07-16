from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm


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
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'core/profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, "You must be logged in to view this page")
        return redirect("home")


# @login_required(login_url='login')
def profile(request, pk):
    if request.user.is_authenticated:
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

    else:
        messages.success(request, "You must be logged in to view this page")
        return redirect("home")
