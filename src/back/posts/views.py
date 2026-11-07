from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Like, Comment, Bookmark
from .forms import PostForm, CommentForm

def post_list(request):
    feed = request.GET.get('feed', 'all')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('home')
    else:
        form = PostForm()
    
    posts_qs = Post.objects.select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    
    if feed == 'following' and request.user.is_authenticated:
        following_ids = request.user.following_relations.values_list('following_id', flat=True)
        posts = posts_qs.filter(author_id__in=following_ids)
    else:
        feed = 'all'
        posts = posts_qs.all()

    context = {
        'posts': posts,
        'form': form,
        'feed': feed,
    }
    return render(request, 'posts/post_list.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'author__profile').prefetch_related('likes', 'comments'),
        id=post_id
    )
    comments = post.comments.select_related('author', 'author__profile').all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, post=post).first()
    
    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes_count,
        })
    
    next_url = request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)

@login_required
def post_bookmark(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    bookmark = Bookmark.objects.filter(user=request.user, post=post).first()

    if bookmark:
        bookmark.delete()
        bookmarked = False
    else:
        Bookmark.objects.create(user=request.user, post=post)
        bookmarked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'bookmarked': bookmarked,
        })

    next_url = request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'posts/post_delete.html', {'post': post})
