from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, #delete the post if the user is deleted
        related_name='posts'
        )
     
    content = models.TextField(verbose_name="Текст допису")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

class Meta:
    ordering = ['-created_at']
    verbose_name = "Допис"
    verbose_name_plural = "Дописи"

def __str__(self):
        return f"{self.author} - {self.content[:20]}..."