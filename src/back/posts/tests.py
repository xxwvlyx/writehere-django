from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Like, Comment, Bookmark
from users.models import Follow

class PostModelAndViewsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password123')
        self.post1 = Post.objects.create(author=self.user1, content='First post content')
        self.post2 = Post.objects.create(author=self.user2, content='Second post content')
        self.client = Client()

    def test_post_str(self):
        self.assertEqual(str(self.post1), f"{self.user1.username} - {self.post1.content[:20]}...")

    def test_post_ordering(self):
        posts = list(Post.objects.all())
        self.assertEqual(posts[0], self.post2)
        self.assertEqual(posts[1], self.post1)

    def test_unauthenticated_post_creation_redirects_to_login(self):
        response = self.client.post(reverse('home'), {'content': 'Unauthorized post'})
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Post.objects.count(), 2)

    def test_authenticated_post_creation(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('home'), {'content': 'New post by user1'})
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Post.objects.count(), 3)
        latest_post = Post.objects.first()
        self.assertEqual(latest_post.content, 'New post by user1')
        self.assertEqual(latest_post.author, self.user1)

    def test_edit_post_permissions(self):
        self.client.login(username='user2', password='password123')
        response = self.client.post(reverse('post_edit', args=[self.post1.id]), {'content': 'Hacked content'})
        self.assertRedirects(response, reverse('home'))
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.content, 'First post content')

        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('post_edit', args=[self.post1.id]), {'content': 'Updated content'})
        self.assertRedirects(response, reverse('post_detail', args=[self.post1.id]))
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.content, 'Updated content')

    def test_delete_post_permissions(self):
        self.client.login(username='user2', password='password123')
        response = self.client.post(reverse('post_delete', args=[self.post1.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Post.objects.filter(id=self.post1.id).exists())

        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('post_delete', args=[self.post1.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())

    def test_like_toggle(self):
        self.client.login(username='user1', password='password123')
        
        # Like post2
        response = self.client.post(reverse('post_like', args=[self.post2.id]))
        self.assertEqual(self.post2.likes_count, 1)
        self.assertTrue(self.post2.is_liked_by(self.user1))

        # Unlike post2
        response = self.client.post(reverse('post_like', args=[self.post2.id]))
        self.assertEqual(self.post2.likes_count, 0)
        self.assertFalse(self.post2.is_liked_by(self.user1))

    def test_comments(self):
        self.client.login(username='user1', password='password123')
        
        # Add comment
        response = self.client.post(reverse('post_detail', args=[self.post2.id]), {'content': 'Great post!'})
        self.assertRedirects(response, reverse('post_detail', args=[self.post2.id]))
        self.assertEqual(self.post2.comments_count, 1)
        comment = self.post2.comments.first()
        self.assertEqual(comment.author, self.user1)
        self.assertEqual(comment.content, 'Great post!')

    def test_bookmarks(self):
        self.client.login(username='user1', password='password123')

        # Bookmark post2
        response = self.client.post(reverse('post_bookmark', args=[self.post2.id]))
        self.assertTrue(self.post2.is_bookmarked_by(self.user1))

        # Remove bookmark
        response = self.client.post(reverse('post_bookmark', args=[self.post2.id]))
        self.assertFalse(self.post2.is_bookmarked_by(self.user1))

    def test_feed_following_filter(self):
        self.client.login(username='user1', password='password123')

        # When not following user2
        response = self.client.get(reverse('home') + '?feed=following')
        self.assertEqual(len(response.context['posts']), 0)

        # Follow user2
        Follow.objects.create(follower=self.user1, following=self.user2)

        # Now following feed should contain post2
        response = self.client.get(reverse('home') + '?feed=following')
        self.assertEqual(len(response.context['posts']), 1)
        self.assertEqual(response.context['posts'][0], self.post2)
