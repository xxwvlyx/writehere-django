from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Користувач"
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name="Про себе")
    location = models.CharField(max_length=100, blank=True, verbose_name="Місцезнаходження")
    website = models.URLField(max_length=200, blank=True, verbose_name="Веб-сайт")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата народження")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name="Обкладинка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"

    def __str__(self):
        return f"Профіль {self.user.username}"

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            try:
                return self.avatar.url
            except ValueError:
                pass
        return f"https://ui-avatars.com/api/?name={self.user.username}&background=0d6efd&color=fff"

    @property
    def cover_url(self):
        if self.cover_image and hasattr(self.cover_image, 'url'):
            try:
                return self.cover_image.url
            except ValueError:
                pass
        return "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&w=800&h=200&q=80"

    @property
    def followers_count(self):
        return self.user.follower_relations.count()

    @property
    def following_count(self):
        return self.user.following_relations.count()

    def is_followed_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.user.follower_relations.filter(follower=user).exists()


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following_relations',
        verbose_name="Хто підписався"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower_relations',
        verbose_name="На кого підписався"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата підписки")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follower_following'),
            models.CheckConstraint(check=~models.Q(follower=models.F('following')), name='prevent_self_follow')
        ]
        ordering = ['-created_at']
        verbose_name = "Підписка"
        verbose_name_plural = "Підписки"

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"
