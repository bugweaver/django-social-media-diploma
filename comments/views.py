from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm


def post_show(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.all()
    if post:
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.post = post
                    comment.user = request.user
                    comment.save()
                    return redirect('post_show', pk=post.pk)
            else:
                form = CommentForm()
        else:
            if request.method == 'POST':
                messages.error(request, "You must be logged in to comment")
                return redirect('login')
            else:
                form = CommentForm()
        return render(request, "comments/post_show.html",
                      {'post': post, 'comments': comments, 'form': form})
    else:
        messages.error(request, "That post does not exist")
        return redirect('home')


def comment_like(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=pk)
        if comment.likes.filter(id=request.user.id):
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You must be logged in to like that comment")
        return redirect('login')


def delete_comment(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=pk)
        if request.user.username == comment.user.username or request.user.id == comment.post.user.id:
            comment.delete()
            messages.success(request, "The comment has been deleted")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You must be logged in")
        return redirect('login')
