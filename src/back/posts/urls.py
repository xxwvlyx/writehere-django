from django.urls import path
from .views import (
    post_list,
    post_detail,
    post_like,
    post_bookmark,
    post_edit,
    post_delete,
)

urlpatterns = [
    path('', post_list, name='home'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', post_like, name='post_like'),
    path('post/<int:post_id>/bookmark/', post_bookmark, name='post_bookmark'),
    path('post/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', post_delete, name='post_delete'),
]

