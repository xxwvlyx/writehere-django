from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор"
    )
    content = models.TextField(blank=True, verbose_name="Текст допису")
    image = models.ImageField(upload_to='post_images/', null=True, blank=True, verbose_name="Зображення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Допис"
        verbose_name_plural = "Дописи"

    def __str__(self):
        text = self.content[:20] if self.content else "[Зображення]"
        return f"{self.author.username} - {text}..."

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

    def is_liked_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()

    def is_bookmarked_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.bookmarks.filter(user=user).exists()


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Користувач"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Допис"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата вподобайки")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_like')
        ]
        ordering = ['-created_at']
        verbose_name = "Вподобайка"
        verbose_name_plural = "Вподобайки"

    def __str__(self):
        return f"{self.user.username} вподобав допис #{self.post_id}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Допис"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор коментаря"
    )
    content = models.TextField(max_length=1000, verbose_name="Текст коментаря")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        ordering = ['created_at']
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"

    def __str__(self):
        return f"{self.author.username} до допису #{self.post_id}: {self.content[:20]}..."


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name="Користувач"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name="Допис"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата збереження")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_bookmark')
        ]
        ordering = ['-created_at']
        verbose_name = "Закладка"
        verbose_name_plural = "Закладки"

    def __str__(self):
        return f"{self.user.username} зберіг допис #{self.post_id}"
