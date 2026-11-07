from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import CustomRegisterForm, CustomLoginForm, ProfileEditForm
from .models import Profile, Follow

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_view(request, username):
    profile_user = get_object_or_404(User.objects.select_related('profile'), username=username)
    user_posts = profile_user.posts.select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    
    context = {
        'profile_user': profile_user,
        'profile': profile_user.profile,
        'user_posts': user_posts,
        'is_following': is_following,
        'followers_count': profile_user.profile.followers_count,
        'following_count': profile_user.profile.following_count,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile)
    
    return render(request, 'users/profile_edit.html', {'form': form, 'profile': profile})

@login_required
def follow_toggle_view(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user == target_user:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Cannot follow yourself'}, status=400)
        return redirect('profile', username=username)

    follow = Follow.objects.filter(follower=request.user, following=target_user).first()
    if follow:
        follow.delete()
        is_following = False
    else:
        Follow.objects.create(follower=request.user, following=target_user)
        is_following = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'is_following': is_following,
            'followers_count': target_user.follower_relations.count(),
        })

    next_url = request.META.get('HTTP_REFERER') or f'/auth/profile/{username}/'
    return redirect(next_url)
