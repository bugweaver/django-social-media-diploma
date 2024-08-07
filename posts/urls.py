from django.urls import path
from . import views

urlpatterns = [
    path('post-like/<int:pk>', views.post_like, name="post_like"),
    path('delete-post/<int:pk>', views.delete_post, name="delete_post"),
    path('edit-post/<int:pk>', views.edit_post, name="edit_post"),
]
