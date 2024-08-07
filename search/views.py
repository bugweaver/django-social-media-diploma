from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from posts.models import Post
from django.contrib.auth.models import User


def search(request):
    if request.method == "POST":
        search = request.POST['search']
        searched_post = Post.objects.filter(body__contains=search)
        searched_user = User.objects.filter(username__contains=search)
        context = {'search': search, 'searched_user': searched_user, 'searched_post': searched_post}
        return render(request, 'search/search.html', context)
    else:
        return render(request, 'search/search.html', {})
