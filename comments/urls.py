from django.urls import path
from . import views

urlpatterns = [
    path('post-show/<int:pk>', views.post_show, name="post_show"),
    path('delete-comment/<int:pk>', views.delete_comment, name="delete_comment"),
]
