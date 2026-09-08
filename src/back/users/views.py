from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .forms import CustomRegisterForm, CustomLoginForm

def register_view(request):
    if request.method == 'POST':
        # Використовуємо CustomRegisterForm замість UserCreationForm
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
        form = CustomLoginForm(data=request.POST) # Використовуємо нову форму
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm() # І тут теж
        
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to a success page after logout

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = profile_user.posts.all()
    
    context = {
        'profile_user': profile_user, 
        'user_posts': user_posts,
    }
    return render(request, 'users/profile.html', context)

