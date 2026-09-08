from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post #our model Post
from .forms import PostForm 

# Create your views here.

def post_list(request):

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)  # Create a new Post object but don't save to the database yet
            new_post.author = request.user  # Set the author to the currently logged-in user
            new_post.save()  # Save the new Post object to the database

        return redirect('home')  # Redirect to the home page after saving the post
    
    else:
        form = PostForm()  # Create an empty f  orm for GET requests
    
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'form': form,
    }

    return render(request, 'posts/post_list.html', context)

@login_required
def post_edit(request, post_id):
    """Редагування допису"""
    # Знаходимо пост за ID
    post = get_object_or_404(Post, id=post_id)
    
    # ПЕРЕВІРКА БЕЗПЕКИ: чи є поточний користувач автором посту?
    if request.user != post.author:
        return redirect('home') # Якщо ні - просто викидаємо його на головну
        
    if request.method == 'POST':
        # Передаємо в форму дані з POST-запиту, АЛЕ вказуємо instance=post, 
        # щоб Django зрозумів, що це оновлення старого, а не створення нового!
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        # Якщо це GET-запит (просто зайшли на сторінку), заповнюємо форму старим текстом
        form = PostForm(instance=post)
        
    return render(request, 'posts/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, post_id):
    """Видалення допису"""
    post = get_object_or_404(Post, id=post_id)
    
    # ПЕРЕВІРКА БЕЗПЕКИ: видаляти може тільки автор
    if request.user != post.author:
        return redirect('home')
        
    if request.method == 'POST':
        # Якщо користувач підтвердив видалення (натиснув кнопку у формі)
        post.delete()
        return redirect('home')
        
    return render(request, 'posts/post_delete.html', {'post': post})