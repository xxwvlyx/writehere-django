from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']  # Only include the content field in the form

        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишіть свій допис тут...',
                'rows': 3,  
                
                }),
        }
