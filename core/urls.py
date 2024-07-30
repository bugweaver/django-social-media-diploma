from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile-list/', views.profile_list, name="profile_list"),
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
]
