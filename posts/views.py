from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post
from .forms import PostForm


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
            form = PostForm(request.POST or None, instance=post)
            if request.method == 'POST':
                if form.is_valid():
                    post = form.save(commit=False)
                    post.user = request.user
                    post.save()
                    messages.success(request, "Your post has been updated")
                    return redirect('home')
            else:
                return render(request, "posts/edit_post.html", {'form': form, "post": post})
        else:
            messages.error(request, "You can't delete a post that is not yours!")
            return redirect('home')

    else:
        messages.error(request, "You must be logged in")
        return redirect('login')
