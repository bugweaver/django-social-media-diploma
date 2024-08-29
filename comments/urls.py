from django.urls import path
from . import views

urlpatterns = [
    path('post-show/<int:pk>', views.post_show, name="post_show"),
    path('clear-scroll-comment-id/', views.clear_scroll_comment_id, name='clear_scroll_comment_id'),
    path('clear-scroll-reply-id/', views.clear_scroll_reply_id, name='clear_scroll_reply_id'),
    path('comment-like/<int:pk>', views.comment_like, name="comment_like"),
    path('delete-comment/<int:pk>', views.delete_comment, name="delete_comment"),
    path('reply-like/<int:pk>', views.reply_like, name="reply_like"),
    path('delete-reply/<int:pk>', views.delete_reply, name="delete_reply"),
]
