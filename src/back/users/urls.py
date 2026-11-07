from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    profile_edit_view,
    follow_toggle_view,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('profile/<str:username>/follow/', follow_toggle_view, name='follow_toggle'),
]
