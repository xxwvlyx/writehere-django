from django.shortcuts import redirect, render
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