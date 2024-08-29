from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Post, Comment, Reply
from .forms import CommentForm, ReplyForm
from django.http import JsonResponse


def clear_scroll_comment_id(request):
    if 'scroll_to_comment' in request.session:
        del request.session['scroll_to_comment']
    return JsonResponse({'status': 'success'})


def clear_scroll_reply_id(request):
    if 'scroll_to_reply' in request.session:
        del request.session['scroll_to_reply']
    return JsonResponse({'status': 'success'})


def post_show(request, pk):
    post = get_object_or_404(Post, id=pk)

    comments = post.comments.all()
    if post:
        form = CommentForm()
        reply_form = ReplyForm()
        if request.user.is_authenticated:
            if request.method == 'POST':
                if 'comment_button' in request.POST:
                    form = CommentForm(request.POST)
                    if form.is_valid():
                        comment = form.save(commit=False)
                        comment.post = post
                        comment.user = request.user
                        comment.save()
                        request.session['scroll_to_comment'] = comment.id
                        return redirect('post_show', pk=post.pk)
                        # return redirect(f"{reverse('post_show', args=[post.pk])}#comment-{comment.id}")

                elif 'reply_button' in request.POST:
                    reply_form = ReplyForm(request.POST)
                    comment_id = request.POST.get('comment_id')
                    if reply_form.is_valid():
                        # print(f"Comment ID: {comment_id}")  # Отладочное сообщение
                        comment = get_object_or_404(Comment, id=comment_id)
                        # print(f"Comment: {comment}")  # Отладочное сообщение
                        reply = reply_form.save(commit=False)
                        reply.parent_comment = comment
                        reply.user = request.user
                        reply.save()
                        # print(f"Reply saved: {reply.content}")  # Отладочное сообщение
                        request.session['scroll_to_reply'] = reply.id
                        return redirect('post_show', pk=post.pk)
                        # return redirect(f"{reverse('post_show', args=[post.pk])}#comment-{comment.id}")

            # else:
            #     form = CommentForm()
            #     reply_form = ReplyForm()
        else:
            if request.method == 'POST':
                messages.error(request, "You must be logged in to comment")
                return redirect('login')
            # else:
            #     form = CommentForm()
            #     reply_form = ReplyForm()
        return render(request, "comments/post_show.html",
                      {'post': post, 'comments': comments, 'form': form, 'reply_form': reply_form})
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


def reply_like(request, pk):
    if request.user.is_authenticated:
        reply = get_object_or_404(Reply, id=pk)
        if reply.likes.filter(id=request.user.id):
            reply.likes.remove(request.user)
        else:
            reply.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You must be logged in to like that comment")
        return redirect('login')


def delete_reply(request, pk):
    if request.user.is_authenticated:
        reply = get_object_or_404(Reply, id=pk)
        if request.user.username == reply.user.username or request.user.id == reply.parent_comment.post.user.id:
            reply.delete()
            messages.success(request, "The comment has been deleted")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You must be logged in")
        return redirect('login')
