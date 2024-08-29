from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from posts.models import Post
from django.contrib.auth.models import User


def search(request):
    query = request.GET.get('q')
    searched_post = Post.objects.filter(body__contains=query)
    searched_user = User.objects.filter(username__contains=query)
    context = {'query': query, 'searched_user': searched_user, 'searched_post': searched_post}
    return render(request, 'search/search.html', context)
