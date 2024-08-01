from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('profiles/', views.profiles, name="profiles"),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update-user/', views.update_user, name='update_user'),
    path('update-password/', views.update_password, name='update_password'),
    path('post-like/<int:pk>', views.post_like, name="post_like"),
    path('post-show/<int:pk>', views.post_show, name="post_show"),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('follow/<int:pk>', views.follow, name="follow"),
    path('delete-post/<int:pk>', views.delete_post, name="delete_post"),
    path('edit-post/<int:pk>', views.edit_post, name="edit_post"),
    path('search', views.search, name="search"),
]
