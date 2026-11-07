from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from users.forms import CustomRegisterForm, CustomLoginForm, ProfileEditForm
from users.backends import EmailOrUsernameModelBackend
from users.models import Profile, Follow

class UsersAppTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', email='other@example.com', password='password123')
        self.client = Client()

    def test_profile_auto_created_by_signal(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)

    def test_custom_register_form_fields(self):
        form = CustomRegisterForm()
        self.assertIn('email', form.fields)
        self.assertTrue(form.fields['email'].required)
        self.assertEqual(form.Meta.fields, ('username', 'email'))
        for field in form.fields.values():
            self.assertIn('form-control', field.widget.attrs.get('class', ''))

    def test_custom_login_form_fields(self):
        form = CustomLoginForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        for field in form.fields.values():
            self.assertIn('form-control', field.widget.attrs.get('class', ''))

    def test_backend_authenticate(self):
        backend = EmailOrUsernameModelBackend()
        # By username
        user = backend.authenticate(None, username='testuser', password='password123')
        self.assertEqual(user, self.user)

        # By email
        user = backend.authenticate(None, username='test@example.com', password='password123')
        self.assertEqual(user, self.user)

        # Invalid password
        user = backend.authenticate(None, username='testuser', password='wrong')
        self.assertIsNone(user)

    def test_follow_toggle_view(self):
        self.client.login(username='testuser', password='password123')

        # Follow other_user
        response = self.client.post(reverse('follow_toggle', args=[self.other_user.username]))
        self.assertTrue(Follow.objects.filter(follower=self.user, following=self.other_user).exists())
        self.assertEqual(self.other_user.profile.followers_count, 1)
        self.assertEqual(self.user.profile.following_count, 1)

        # Unfollow other_user
        response = self.client.post(reverse('follow_toggle', args=[self.other_user.username]))
        self.assertFalse(Follow.objects.filter(follower=self.user, following=self.other_user).exists())
        self.assertEqual(self.other_user.profile.followers_count, 0)
        self.assertEqual(self.user.profile.following_count, 0)

    def test_cannot_follow_self(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('follow_toggle', args=[self.user.username]))
        self.assertFalse(Follow.objects.filter(follower=self.user, following=self.user).exists())

    def test_profile_edit_view(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'first_name': 'Олександр',
            'last_name': 'Тестовий',
            'bio': 'Нова біографія користувача',
            'location': 'Київ',
            'website': 'https://example.com',
            'birth_date': '1995-05-15',
        }
        response = self.client.post(reverse('profile_edit'), data)
        self.assertRedirects(response, reverse('profile', args=['testuser']))
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Олександр')
        self.assertEqual(self.user.profile.bio, 'Нова біографія користувача')
        self.assertEqual(self.user.profile.location, 'Київ')
        self.assertEqual(self.user.profile.website, 'https://example.com')
